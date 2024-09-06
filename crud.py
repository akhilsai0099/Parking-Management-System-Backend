from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import HTTPException
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
    try:
        db_spot = models.ParkingSpot(**parking_spot.model_dump())
        db.add(db_spot)
        db.commit()
        db.refresh(db_spot)
        return db_spot
    except IntegrityError as e:
        if "unique" in str(e).lower():
            raise HTTPException(status_code=400, detail="Parking spot already exists")
        raise e

def update_parking_spot(db: Session, spot_id: int, parking_spot: schemas.ParkingSpotCreate):
    db_spot = db.query(models.ParkingSpot).filter(models.ParkingSpot.id == spot_id).first()
    if not db_spot:
        raise HTTPException(status_code=404, detail="Parking spot not found")
    existing_spot = db.query(models.ParkingSpot).filter((models.ParkingSpot.level == parking_spot.level) &
                                                       (models.ParkingSpot.section == parking_spot.section) &
                                                       (models.ParkingSpot.spot_number == parking_spot.spot_number)).first()
    if existing_spot and existing_spot.id != spot_id:
        raise HTTPException(status_code=400, detail="Parking spot already exists")
    for var, value in vars(parking_spot).items():
        setattr(db_spot, var, value) if value else None
    db.add(db_spot)
    db.commit()
    db.refresh(db_spot)
    return db_spot

def delete_parking_spot(db: Session, spot_id: int):
    db_spot = db.query(models.ParkingSpot).filter(models.ParkingSpot.id == spot_id).first()
    if not db_spot:
        raise HTTPException(status_code=404, detail="Parking spot not found")
    db.delete(db_spot)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Parking spot deleted"})
def get_parking_spots(db: Session):
    return db.query(models.ParkingSpot).all()


def create_vehicle(request: Request, db: Session, vehicle: schemas.VehicleCreate):
    user = get_user_by_email(db, request.state.curr_user)
    vehicle.owner_id = user.id
    db_vehicle = models.Vehicle(**vehicle.model_dump())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def update_vehicle(request: Request, id: int,vehicle: schemas.VehicleCreate ,db: Session):
    user = get_user_by_email(db, request.state.curr_user)
    db_vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == id, models.Vehicle.owner_id == user.id).first()
    if not db_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    for var, value in vars(vehicle).items():
        setattr(db_vehicle, var, value) if value else None
    print("here")
    db.commit()
    return db_vehicle
def delete_vehicle(request: Request, id: int ,db: Session):
    user = get_user_by_email(db, request.state.curr_user)
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == id, models.Vehicle.owner_id == user.id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    db.delete(vehicle)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Vehicle deleted"})

def get_vehicles(request:Request,db: Session):
    user_id = get_user_by_email(db, request.state.curr_user).id
    return db.query(models.Vehicle).filter(models.Vehicle.owner_id ==user_id).all()


def get_vehicle_by_license_plate(db: Session, license_plate: str):
    return db.query(models.Vehicle).filter(models.Vehicle.license_plate == license_plate).first()

def create_parking_session(db: Session, session: schemas.ParkingSessionCreate):
    vehicle = get_vehicle_by_license_plate(db, session.license_plate)
    session.vehicle_id = vehicle.id
    db_session = models.ParkingSession(**session.model_dump())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session
