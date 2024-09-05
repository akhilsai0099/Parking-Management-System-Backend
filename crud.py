from sqlalchemy.orm import Session
import models, schemas
from helpers.passwordHash import get_password_hash 

def create_user(db: Session, user: schemas.UserCreate):
    user.password = get_password_hash(user.password)
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_parking_spot(db: Session, parking_spot: schemas.ParkingSpotCreate):
    db_spot = models.ParkingSpot(**parking_spot.model_dump())
    db.add(db_spot)
    db.commit()
    db.refresh(db_spot)
    return db_spot

def get_parking_spots(db: Session):
    return db.query(models.ParkingSpot).all()


def create_vehicle(db: Session, vehicle: schemas.VehicleCreate):
    db_vehicle = models.Vehicle(**vehicle.model_dump())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def get_vehicles(db: Session):
    return db.query(models.Vehicle).all()


def create_parking_session(db: Session, session: schemas.ParkingSessionCreate):
    db_session = models.ParkingSession(**session.model_dump())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session
