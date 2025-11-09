from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP, text, Boolean, Float, JSON, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(String, nullable=False, default="user")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class OTP(Base):
    __tablename__ = 'otps'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, ForeignKey('users.email'))
    otp = Column(String, nullable=False)

class FloorPlan(Base):
    __tablename__ = "floor_plans"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=True)
    building = Column(String, nullable=True)
    floor_number = Column(Integer, nullable=True)
    image_path = Column(String, nullable=False)     #s3/minio key or local path
    pixels_per_meter = Column(Float, nullable=True)
    units = Column(String, default="meters")
    version = Column(Integer, default=1)
    uploaded_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    overlays = relationship("Overlay", back_populates="floor_plan", cascade="all, delete-orphan")
    versions = relationship("FloorPlanVersion", back_populates="floor_plan", cascade="all, delete-orphan")

class Overlay(Base):
    __tablename__ = "overlays"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    floor_plan_id = Column(Integer, ForeignKey("floor_plans.id", ondelete="CASCADE"), nullable=False)
    type = Column(String, nullable=False)           #'room' or 'seat'
    label = Column(String, nullable=True)
    capacity = Column(Integer, nullable=True)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    props = Column(JSON, default={})
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    floor_plan = relationship("FloorPlan", back_populates="overlays")

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    overlay_id = Column(Integer, ForeignKey("overlays.id", ondelete="CASCADE"), nullable=False)
    organizer_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    start_ts = Column(DateTime, nullable=False)
    end_ts = Column(DateTime, nullable=False)
    participants = Column(Integer, nullable=True)
    status = Column(String, default="confirmed")   #confirmed / cancelled / pending
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class FloorPlanVersion(Base):
    __tablename__ = "floorplan_versions"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    floor_plan_id = Column(Integer, ForeignKey("floor_plans.id", ondelete="CASCADE"), nullable=False)
    version = Column(Integer, nullable=False)
    changes = Column(JSON, nullable=True)          #snapshot or json patch
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    floor_plan = relationship("FloorPlan", back_populates="versions")

    __table_args__ = (UniqueConstraint('floor_plan_id', 'version', name='uix_floorplan_version'),)    