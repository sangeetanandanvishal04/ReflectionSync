from fastapi import APIRouter, status, HTTPException, Depends
from ..database import get_db
from sqlalchemy.orm import Session

from .. import schemas, tablesmodel, oAuth2

router = APIRouter(tags=['Admin'])

#Use to get the currently authenticated user's info
@router.get("/me", response_model=schemas.UserOut)
def read_current_user(current_user: tablesmodel.User = Depends(oAuth2.get_current_user)):
    return current_user

#Used by Admin to promote user to admin
#http://127.0.0.1:8000/admin/promote?email=user@gmail.com
@router.post("/admin/promote")
def promote_user_to_admin(email: str, db: Session = Depends(get_db), admin_user: tablesmodel.User = Depends(oAuth2.require_admin)):
    user = db.query(tablesmodel.User).filter(tablesmodel.User.email == email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user.role = "admin"
    db.commit()
    return {"message": f"{email} promoted to admin"}