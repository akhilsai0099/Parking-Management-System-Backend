from fastapi import FastAPI, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
import models, crud, schemas
from database import engine, SessionLocal, init_db
from helpers.passwordHash import verify_password
from jwtToken import create_access_token

init_db()

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/register/", response_model=schemas.UserCreate)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/login/", response_model=schemas.Token)
def login(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user or verify_password(user.password, db_user.password) is False:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    token = create_access_token(data={"username": db_user.email})
    return {"token": token, "role": db_user.role}

@app.post("/parking_spots/", response_model=schemas.ParkingSpot)
def create_parking_spot(parking_spot: schemas.ParkingSpotCreate, db: Session = Depends(get_db)):
    return crud.create_parking_spot(db=db, parking_spot=parking_spot)

@app.get("/parking_spots/", response_model=list[schemas.ParkingSpot])
def read_parking_spots(db: Session = Depends(get_db)):
    return crud.get_parking_spots(db=db)

@app.post("/vehicles/", response_model=schemas.Vehicle)
def create_vehicle(vehicle: schemas.VehicleCreate, db: Session = Depends(get_db)):
    return crud.create_vehicle(db=db, vehicle=vehicle)

@app.get("/vehicles/", response_model=list[schemas.Vehicle])
def read_vehicles(db: Session = Depends(get_db)):
    return crud.get_vehicles(db=db)

@app.post("/parking_sessions/", response_model=schemas.ParkingSession)
def create_parking_session(session: schemas.ParkingSessionCreate, db: Session = Depends(get_db)):
    return crud.create_parking_session(db=db, session=session)
	