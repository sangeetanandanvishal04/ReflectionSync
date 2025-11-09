from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, tablesmodel, oAuth2
from ..database import get_db
from ..services import storage

router = APIRouter(prefix="/floorplans", tags=["floorplans"])

@router.post("", response_model=schemas.FloorPlanOut)
def upload_floorplan(file: UploadFile = File(...), name: str = Form(None), building: str = Form(None), floor_number: int = Form(None), 
                     pixels_per_meter: float = Form(None), db: Session = Depends(get_db), current_user: tablesmodel.User = Depends(oAuth2.get_current_user)):
    
    path = storage.save_upload_local(file)
    fp = tablesmodel.FloorPlan(
        name=name,
        building=building,
        floor_number=floor_number,
        image_path=path,
        pixels_per_meter=pixels_per_meter,
        uploaded_by=current_user.id if current_user else None,
    )

    db.add(fp)
    db.commit()
    db.refresh(fp)
    return fp

@router.get("", response_model=List[schemas.FloorPlanOut])
def list_floorplans(db: Session = Depends(get_db)):
    fps = db.query(tablesmodel.FloorPlan).order_by(tablesmodel.FloorPlan.created_at.desc()).all()
    return fps

@router.get("/{id}", response_model=schemas.FloorPlanOut)
def get_floorplan(id: int, db: Session = Depends(get_db)):
    fp = db.query(tablesmodel.FloorPlan).filter(tablesmodel.FloorPlan.id == id).first()

    if not fp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Floorplan not found")
    return fp

@router.put("/{id}/save")
def save_overlays(id: int, payload: schemas.SaveOverlays, db: Session = Depends(get_db), current_user: tablesmodel.User = Depends(oAuth2.get_current_user)):
    fp = db.query(tablesmodel.FloorPlan).filter(tablesmodel.FloorPlan.id == id).first()
    if not fp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Floorplan not found")

    #lock check (optimistic)
    if payload.client_version != fp.version:
        server_overlays = db.query(tablesmodel.Overlay).filter(tablesmodel.Overlay.floor_plan_id == fp.id).all()
        
        server_overlays_json = []
        for o in server_overlays:
            server_overlays_json.append({
                "id": o.id,
                "type": o.type,
                "label": o.label,
                "capacity": o.capacity,
                "x": o.x,
                "y": o.y,
                "width": o.width,
                "height": o.height,
                "props": o.props,
                "created_by": o.created_by,
                "created_at": o.created_at.isoformat() if o.created_at is not None else None
            })

        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={
            "message": "version_mismatch",
            "server_version": fp.version,
            "server_overlays": server_overlays_json
        })

    #delete old overlays and insert new ones
    db.query(tablesmodel.Overlay).filter(tablesmodel.Overlay.floor_plan_id == fp.id).delete()
    db.commit()

    for ov in payload.overlays:
        new_ov = tablesmodel.Overlay(
            floor_plan_id=fp.id,
            type=ov.type,
            label=ov.label,
            capacity=ov.capacity,
            x=ov.x,
            y=ov.y,
            width=ov.width,
            height=ov.height,
            props=ov.props,
            created_by=current_user.id if current_user else None
        )
        db.add(new_ov)

    fp.version = fp.version + 1
    version_entry = tablesmodel.FloorPlanVersion(
        floor_plan_id=fp.id,
        version=fp.version,
        changes={"overlays": [ov.dict() for ov in payload.overlays]},
        created_by=current_user.id if current_user else None
    )

    db.add(version_entry)
    db.commit()
    db.refresh(fp)
    return {"status": "ok", "new_version": fp.version}

@router.get("/{id}/versions")
def list_versions(id: int, db: Session = Depends(get_db)):
    fp = db.query(tablesmodel.FloorPlan).filter(tablesmodel.FloorPlan.id == id).first()
    if not fp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Floorplan not found")
    
    versions = db.query(tablesmodel.FloorPlanVersion).filter(tablesmodel.FloorPlanVersion.floor_plan_id == id).order_by(tablesmodel.FloorPlanVersion.version.desc()).all()
    return [{"version": v.version, "changes": v.changes, "created_at": v.created_at} for v in versions]