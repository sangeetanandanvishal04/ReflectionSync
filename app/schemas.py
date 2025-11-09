from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List, Dict

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    email: EmailStr
    created_at: datetime
    role: str

    class Config:
        from_attributes = True 

class UserLogin(BaseModel):
    email: EmailStr
    password: str     

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    role: Optional[str] = None

class PasswordChange(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str

class PasswordReset(BaseModel):
    email: EmailStr
    new_password: str
    confirm_password: str   

class OTP(BaseModel):
    email: EmailStr
    otp: str

class FloorPlanCreate(BaseModel):
    name: Optional[str]
    building: Optional[str]
    floor_number: Optional[int]
    pixels_per_meter: Optional[float]

class FloorPlanOut(BaseModel):
    id: int
    name: Optional[str]
    building: Optional[str]
    floor_number: Optional[int]
    image_path: str
    pixels_per_meter: Optional[float]
    version: int
    uploaded_by: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True

class OverlayBase(BaseModel):
    type: str
    label: Optional[str]
    capacity: Optional[int]
    x: int
    y: int
    width: int
    height: int
    props: Optional[Dict] = {}

class OverlayCreate(OverlayBase):
    floor_plan_id: int

class OverlayOut(OverlayBase):
    id: int
    floor_plan_id: int
    created_by: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True

class SaveOverlays(BaseModel):
    floor_plan_id: int
    client_version: int
    overlays: List[OverlayBase]

class BookingCreate(BaseModel):
    overlay_id: int
    start_ts: datetime
    end_ts: datetime
    participants: Optional[int]

class BookingOut(BookingCreate):
    id: int
    organizer_id: Optional[int]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True