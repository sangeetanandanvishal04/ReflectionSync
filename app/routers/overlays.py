from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, tablesmodel, oAuth2
from ..database import get_db

router = APIRouter(prefix="/overlays", tags=["overlays"])

# POST /overlays
# Body: OverlayCreate
@router.post("", response_model=schemas.OverlayOut)
def create_overlay(payload: schemas.OverlayCreate, db: Session = Depends(get_db), current_user: tablesmodel.User = Depends(oAuth2.get_current_user)):
    fp = db.query(tablesmodel.FloorPlan).filter(tablesmodel.FloorPlan.id == payload.floor_plan_id).first()
    if not fp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Floorplan not found")

    ov = tablesmodel.Overlay(
        floor_plan_id=payload.floor_plan_id,
        type=payload.type,
        label=payload.label,
        capacity=payload.capacity,
        x=payload.x,
        y=payload.y,
        width=payload.width,
        height=payload.height,
        props=payload.props,
        created_by=current_user.id if current_user else None
    )
    db.add(ov)
    db.commit()
    db.refresh(ov)
    return ov

# PUT /overlays/{id}
# Body: OverlayBase (update fields)
@router.put("/{id}", response_model=schemas.OverlayOut)
def update_overlay(id: int, payload: schemas.OverlayBase, db: Session = Depends(get_db), current_user: tablesmodel.User = Depends(oAuth2.get_current_user)):
    ov = db.query(tablesmodel.Overlay).filter(tablesmodel.Overlay.id == id).first()
    if not ov:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Overlay not found")
    ov.type = payload.type
    ov.label = payload.label
    ov.capacity = payload.capacity
    ov.x = payload.x
    ov.y = payload.y
    ov.width = payload.width
    ov.height = payload.height
    ov.props = payload.props
    db.commit()
    db.refresh(ov)
    return ov

# DELETE /overlays/{id}
@router.delete("/{id}")
def delete_overlay(id: int, db: Session = Depends(get_db), current_user: tablesmodel.User = Depends(oAuth2.get_current_user)):
    ov = db.query(tablesmodel.Overlay).filter(tablesmodel.Overlay.id == id).first()
    if not ov:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Overlay not found")
    db.delete(ov)
    db.commit()
    return {"message": "overlay deleted"}

# GET /floorplans/{id}/overlays
@router.get("/floorplan/{floorplan_id}", response_model=List[schemas.OverlayOut])
def list_overlays_for_floorplan(floorplan_id: int, db: Session = Depends(get_db)):
    overlays = db.query(tablesmodel.Overlay).filter(tablesmodel.Overlay.floor_plan_id == floorplan_id).all()
    return overlays