from fastapi import FastAPI, Depends, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse, Response
import jwt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import  crud, schemas
from database import engine, SessionLocal, init_db
from helpers.passwordHash import verify_password
from jwtToken import create_access_token
from middleware import get_current_user
import logging
from logging.handlers import RotatingFileHandler

init_db()

app = FastAPI()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler('app.log', maxBytes=1024*1024*10, backupCount=5)
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.middleware("http")
async def authMiddleware(request: Request, call_next):
    if request.url.path in ["/login/", "/register/"]:
        return await call_next(request)
    if "Authorization" in request.headers:
        try:
            curr_user = get_current_user(request.headers["Authorization"].split(" ")[1])
        except HTTPException as e:
            logger.error(e)
            return JSONResponse(status_code=e.status_code, content={"message": e.detail})
    else:
        logger.error("Unauthorized request")
        return JSONResponse(status_code=403, content={"message": "Unauthorized"})

    
    if curr_user:
        request.state.curr_user = curr_user
        response = await call_next(request)
    return response

def get_logs():
    with open('app.log', 'r') as f:
        return f.readlines()

@app.get("/logs/")
async def read_logs():
    logs = get_logs()
    return Response(content='\n'.join(logs[::-1]), media_type="text/plain")

@app.post("/register/", response_model=schemas.UserCreate)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        logger.error(f"Email {user.email} already registered")
        return JSONResponse(status_code=400, content={"message": "Email already registered"})
    logger.info(f"User {user.email} registered")
    return crud.create_user(db=db, user=user)

@app.post("/login/", response_model=schemas.Token)
def login(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user or verify_password(user.password, db_user.password) is False:
        logger.error(f"Invalid email or password for user {user.email}")
        return JSONResponse(status_code=400, content={"message": "Invalid email or password"})
    token = create_access_token(data={"email": db_user.email})
    logger.info(f"User {user.email} logged in")
    return {"token": token, "role": db_user.is_admin}

@app.post("/parking_spots/", response_model=schemas.ParkingSpot)
def create_parking_spot(parking_spot: schemas.ParkingSpotCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating parking spot {parking_spot.spot_number}")
    try:
        return crud.create_parking_spot(db=db, parking_spot=parking_spot)
    except IntegrityError as e:
        if "unique" in str(e).lower():
            logger.error(f"Parking spot {parking_spot.spot_number} already exists")
            return JSONResponse(status_code=400, content={"message": "Parking spot already exists"})
        raise e

@app.put("/parking_spots/{spot_id}")
def update_parking_spot(spot_id: int, parking_spot: schemas.ParkingSpotCreate, db: Session = Depends(get_db)):
    logger.info(f"Updating parking spot {spot_id}")
    try:
        return crud.update_parking_spot(db=db, spot_id=spot_id, parking_spot=parking_spot)
    except HTTPException as e:
            logger.error(f"Parking spot {parking_spot.spot_number} already exists")
            return  JSONResponse(status_code=e.status_code, message=e.detail)

@app.delete("/parking_spots/{spot_id}")
def delete_parking_spot(spot_id: int, db: Session = Depends(get_db)):
    logger.info(f"Deleting parking spot {spot_id}")
    try:
        return crud.delete_parking_spot(db=db, spot_id=spot_id)
    except HTTPException as e:
        logger.error(f"Parking spot {spot_id} not found")
        return JSONResponse(status_code=e.status_code, message=e.detail)

@app.get("/parking_spots/", response_model=list[schemas.ParkingSpot])
def read_parking_spots(db: Session = Depends(get_db)):
    logger.info("Fetching all parking spots")
    return crud.get_parking_spots(db=db)

@app.get("/parking_spots/availability/level/{level}", response_model=list[schemas.ParkingSpot])
def read_parking_spots_by_level(level: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching parking spots by level {level}")
    return crud.get_parking_spots_by_level(db=db, level=level)

@app.get("/parking_spots/availability/section/{section}", response_model=list[schemas.ParkingSpot])
def read_parking_spots_by_section(section: str, db: Session = Depends(get_db)):
    logger.info(f"Fetching parking spots by section {section}")
    return crud.get_parking_spots_by_section(db=db, section=section)

@app.post("/vehicles/", response_model=schemas.Vehicle)
def create_vehicle(request:Request, vehicle: schemas.VehicleCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating vehicle {vehicle.license_plate}")
    return crud.create_vehicle(request,db=db, vehicle=vehicle)

@app.get("/vehicles/", response_model=list[schemas.Vehicle])
def read_vehicles(request: Request, db: Session = Depends(get_db)):
    logger.info(f"Fetching all vehicles")
    return crud.get_vehicles(request,db=db)

@app.put("/vehicles/{id}")
def edit_vehicle(request: Request, id: int, vehicle: schemas.VehicleCreate ,db: Session = Depends(get_db)):
    try:
        crud.update_vehicle(request, id=id, vehicle=vehicle ,db=db)
        logger.info(f"Updating vehicle {id}")
        return JSONResponse(status_code=200, content={"message": "Vehicle updated"})
    except HTTPException as e:
        logger.error(f"{e.status_code}, {e.detail}")
        return  JSONResponse(status_code=e.status_code, message=e.detail)

@app.delete("/vehicles/{id}", response_model=list[schemas.Vehicle])
def delete_vehicle(request: Request, id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_vehicle(request, id=id, db=db)
        logger.info(f"Deleting vehicle {id}")
        return JSONResponse(status_code=200, content={"message": "Vehicle deleted"})
    except HTTPException as e:
        logger.error(f"{e.status_code}, {e.detail}")
        return  JSONResponse(status_code=e.status_code, message=e.detail)

@app.post("/parking_sessions/")
def create_parking_session(session: schemas.ParkingSessionCreate, db: Session = Depends(get_db)):
    try:
        crud.create_parking_session(db=db, session=session)
        logger.info(f"Creating parking session {session.vehicle_id}")
        return JSONResponse(status_code=200, content={"message": "Parking session created"})
    except ValueError as e:
        logger.error(e)
        return JSONResponse(status_code=400, content={"message": str(e)})
    except HTTPException as e:
        logger.error(f"{e.status_code}, {e.detail}")
        return JSONResponse(status_code=e.status_code, content={"message": e.detail})
    
@app.delete("/parking_sessions/{session_id}")
def delete_parking_session(session_id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_parking_session(db=db, session_id=session_id)
        logger.info(f"Deleting parking session {session_id}")
        return JSONResponse(status_code=200, content={"message": "Parking session deleted"})
    except HTTPException as e:
        logger.error(f"Parking session {session_id} not found")
        return JSONResponse(status_code=e.status_code, content={"message": e.detail})

@app.get("/parking_sessions/", response_model=list[schemas.ParkingSession])
def get_parking_sessions(db: Session = Depends(get_db)):
    logger.info(f"Fetching all parking sessions")
    return crud.get_parking_sessions(db=db)

@app.get("/parking_sessions/revenue")
def calculate_total_revenue(db: Session = Depends(get_db)):
    logger.info("Calculating total revenue")
    return crud.calculate_total_revenue(db=db)

@app.put("/parking_sessions/{session_id}/price", response_model=schemas.Price)
def calculate_price_and_exit(session_id: int, db: Session = Depends(get_db)):
    try:
        ans = crud.calculate_price_and_exit(db=db, session_id=session_id)
        logger.info(f"Calculating price of parking session {session_id}")
        return ans
    except HTTPException as e:
        logger.error(f"{e.status_code}, {e.detail}")
        return JSONResponse(status_code=e.status_code, content={"message": e.detail})

