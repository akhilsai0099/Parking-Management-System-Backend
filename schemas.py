from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class User(BaseModel):
    email: EmailStr
    password: str

class UserCreate(User):
    pass

class ParkingSpotBase(BaseModel):
    level: int
    section: str
    spot_number: int
    vehicle_type: str
    is_occupied: bool

class ParkingSpotCreate(ParkingSpotBase):
    pass

class ParkingSpot(ParkingSpotBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class VehicleBase(BaseModel):
    license_plate: str
    vehicle_type: str
    owner_id: Optional[int] = None
    owner_name: str
    contact_number: str

class VehicleCreate(VehicleBase):
    pass

class Vehicle(VehicleBase):
    id: int
    license_plate: str

    class Config:
        orm_mode = True

class ParkingSessionBase(BaseModel):
    vehicle_id: int
    spot_id: Optional[int] = None
    expected_exit_time: datetime

class ParkingSessionCreate(ParkingSessionBase):
    vehicle_id: int
    entry_time: datetime


class ParkingSession(ParkingSessionBase):
    id: int
    entry_time: datetime
    actual_exit_time: Optional[datetime] = None
    fee: Optional[float] = None
    payment_status: str
    created_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    token: str
    role: bool