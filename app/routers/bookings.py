from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from .. import schemas, tablesmodel, oAuth2
from ..database import get_db

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.post("", response_model=schemas.BookingOut)
def create_booking(payload: schemas.BookingCreate, db: Session = Depends(get_db), current_user: tablesmodel.User = Depends(oAuth2.get_current_user)):
    overlay = db.query(tablesmodel.Overlay).filter(tablesmodel.Overlay.id == payload.overlay_id).first()
    if not overlay:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Overlay (room) not found")

    #conflict check
    overlapping = db.query(tablesmodel.Booking).filter(
        tablesmodel.Booking.overlay_id == payload.overlay_id,
        ~(
            (tablesmodel.Booking.end_ts <= payload.start_ts) |
            (tablesmodel.Booking.start_ts >= payload.end_ts)
        )
    ).all()

    if overlapping:
        conflicts = []
        for b in overlapping:
            conflicts.append({
                "id": b.id,
                "start_ts": b.start_ts.isoformat() if isinstance(b.start_ts, datetime) else str(b.start_ts),
                "end_ts": b.end_ts.isoformat() if isinstance(b.end_ts, datetime) else str(b.end_ts),
                "organizer_id": b.organizer_id
            })

        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={
            "message": "booking_conflict",
            "conflicts": conflicts
        })

    #no conflict, book it
    b = tablesmodel.Booking(
        overlay_id=payload.overlay_id,
        organizer_id=current_user.id if current_user else None,
        start_ts=payload.start_ts,
        end_ts=payload.end_ts,
        participants=payload.participants,
        status="confirmed"
    )
    
    db.add(b)
    db.commit()
    db.refresh(b)
    return b

@router.get("/{id}", response_model=schemas.BookingOut)
def get_booking(id: int, db: Session = Depends(get_db), current_user: tablesmodel.User = Depends(oAuth2.get_current_user)):
    b = db.query(tablesmodel.Booking).filter(tablesmodel.Booking.id == id).first()
    if not b:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    return b

@router.get("/overlay/{overlay_id}", response_model=List[schemas.BookingOut])
def list_bookings_for_overlay(overlay_id: int, db: Session = Depends(get_db)):
    bs = db.query(tablesmodel.Booking).filter(tablesmodel.Booking.overlay_id == overlay_id).order_by(tablesmodel.Booking.start_ts).all()
    return bs

@router.get("/available")
def available_rooms(start: datetime = Query(...), end: datetime = Query(...), capacity: Optional[int] = Query(None), db: Session = Depends(get_db)):
    #start/end are required query params (ISO datetime)
    q = db.query(tablesmodel.Overlay).filter(tablesmodel.Overlay.type == "room") #find candidate rooms (type='room')
    
    if capacity is not None:
        q = q.filter(tablesmodel.Overlay.capacity >= capacity)
    candidates = q.all()
    available = []

    for candidate in candidates:
        overlapping = db.query(tablesmodel.Booking).filter(
            tablesmodel.Booking.overlay_id == candidate.id,
            ~(
                (tablesmodel.Booking.end_ts <= start) |
                (tablesmodel.Booking.start_ts >= end)
            )
        ).count()
        if overlapping == 0:
            available.append(candidate)

    return [ {
        "id": o.id,
        "floor_plan_id": o.floor_plan_id,
        "type": o.type,
        "label": o.label,
        "capacity": o.capacity,
        "x": o.x,
        "y": o.y,
        "width": o.width,
        "height": o.height,
        "props": o.props
    } for o in available ]