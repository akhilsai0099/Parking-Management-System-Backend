import datetime
from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import HTTPException
import models, schemas
from helpers.passwordHash import get_password_hash 
import math

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
        print(var,value)
        setattr(db_spot, var, value) if value is not None else None
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

def get_parking_spots_by_level(db: Session, level: int):
    return db.query(models.ParkingSpot).filter((models.ParkingSpot.level == level) & (models.ParkingSpot.is_occupied == False)).all()

def get_parking_spots_by_section(db: Session, section: str):
    return db.query(models.ParkingSpot).filter((models.ParkingSpot.section == section) & (models.ParkingSpot.is_occupied == False)).all()


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
        setattr(db_vehicle, var, value) if value is not None else None
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

def get_parking_sessions(db: Session):
    return db.query(models.ParkingSession).all()

def delete_parking_session(db: Session, session_id: int):
    db_session = db.query(models.ParkingSession).filter(models.ParkingSession.id == session_id).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Parking session not found")
    db.delete(db_session)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Parking session deleted"})

def create_parking_session(db: Session, session: schemas.ParkingSessionCreate):
    time_diff = session.expected_exit_time - session.entry_time
    vehicle = db.query(models.ParkingSession).filter(models.ParkingSession.vehicle_id == session.vehicle_id,
                                                     models.ParkingSession.actual_exit_time == None).first()
    if vehicle:
        raise HTTPException(status_code=404, detail="Vehicle Didn't Previously exit")
    
    if time_diff.total_seconds() / 3600 <= 1:
        best_spot = db.query(models.ParkingSpot).filter(
            models.ParkingSpot.is_occupied == False,
            models.ParkingSpot.vehicle_type == db.query(models.Vehicle).filter(models.Vehicle.id == session.vehicle_id).first().vehicle_type,
            models.ParkingSpot.short_term_only == True
        ).order_by(models.ParkingSpot.exit_distance).first()
        if best_spot is None:
            best_spot = db.query(models.ParkingSpot).filter(
                models.ParkingSpot.is_occupied == False,
                models.ParkingSpot.vehicle_type == db.query(models.Vehicle).filter(models.Vehicle.id == session.vehicle_id).first().vehicle_type
            ).order_by(models.ParkingSpot.exit_distance).first()
    else:
        best_spot = db.query(models.ParkingSpot).filter(
            models.ParkingSpot.is_occupied == False,
            models.ParkingSpot.vehicle_type == db.query(models.Vehicle).filter(models.Vehicle.id == session.vehicle_id).first().vehicle_type,
            models.ParkingSpot.short_term_only == False
        ).order_by(models.ParkingSpot.exit_distance).first()

    if not best_spot:
        raise ValueError("No available parking spots")

    best_spot.is_occupied = True
    session.spot_id = best_spot.id

    db_session = models.ParkingSession(**session.model_dump())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)

    return db_session

def calculate_price_and_exit(db: Session, session_id: int):
    db_session = db.query(models.ParkingSession).filter(models.ParkingSession.id == session_id).first()
    if db_session.payment_status == "Paid":
        return {"price": db_session.fee}
    if not db_session:
        raise HTTPException(status_code=404, detail="Parking session not found")
    total_minutes = (min(datetime.datetime.now(), db_session.expected_exit_time) - db_session.entry_time).total_seconds() / 60
    total_quarters = math.ceil(total_minutes / 15)
    price = total_quarters * 1
    if datetime.datetime.now() > db_session.expected_exit_time:
        extra_minutes = (datetime.datetime.now() - db_session.expected_exit_time).total_seconds() / 60
        extra_quarters = math.ceil(extra_minutes / 15)
        price += extra_quarters * 2
    db_session.fee = price
    db_session.payment_status = "Paid"
    db_session.actual_exit_time = datetime.datetime.now()
    spot = db.query(models.ParkingSpot).filter(models.ParkingSpot.id == db_session.spot_id).first()
    spot.is_occupied = False
    db.commit()
    return {"price": price}
