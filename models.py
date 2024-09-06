from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)


class ParkingSpot(Base):
    __tablename__ = "parking_spots"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(Integer)
    section = Column(String)
    spot_number = Column(Integer)
    vehicle_type = Column(String)
    is_occupied = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())

    __table_args__ = (UniqueConstraint('level', 'section', 'spot_number', name='unique_level_section_spot'),)

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    license_plate = Column(String, unique=True, index=True)
    vehicle_type = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner_name = Column(String)
    contact_number = Column(String)
    created_at = Column(DateTime, default=datetime.now())

class ParkingSession(Base):
    __tablename__ = "parking_sessions"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'))
    spot_id = Column(Integer, ForeignKey('parking_spots.id'))
    entry_time = Column(DateTime, default=datetime.now())
    expected_exit_time = Column(DateTime)
    actual_exit_time = Column(DateTime, nullable=True)
    fee = Column(Integer, nullable=True)
    payment_status = Column(String, default="Pending")

    vehicle = relationship("Vehicle")
    spot = relationship("ParkingSpot")
