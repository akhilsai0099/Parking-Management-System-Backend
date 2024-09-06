from fastapi import FastAPI, Depends, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse 
from sqlalchemy.orm import Session
import  crud, schemas
from database import engine, SessionLocal, init_db
from helpers.passwordHash import verify_password
from jwtToken import create_access_token
from middleware import get_current_user

init_db()

app = FastAPI()

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
    try:
        curr_user = get_current_user(request.headers["Authorization"].split(" ")[1])
    except HTTPException:
        return JSONResponse(status_code=403, content={"message": "Unauthorized"})
    if curr_user:
        request.state.curr_user = curr_user
        response = await call_next(request)
    return response

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
    token = create_access_token(data={"email": db_user.email})
    return {"token": token, "role": db_user.is_admin}

@app.post("/parking_spots/", response_model=schemas.ParkingSpot)
def create_parking_spot(parking_spot: schemas.ParkingSpotCreate, db: Session = Depends(get_db)):
    return crud.create_parking_spot(db=db, parking_spot=parking_spot)

@app.put("/parking_spots/{spot_id}")
def update_parking_spot(spot_id: int, parking_spot: schemas.ParkingSpotCreate, db: Session = Depends(get_db)):
    return crud.update_parking_spot(db=db, spot_id=spot_id, parking_spot=parking_spot)

@app.delete("/parking_spots/{spot_id}")
def delete_parking_spot(spot_id: int, db: Session = Depends(get_db)):
    return crud.delete_parking_spot(db=db, spot_id=spot_id)

@app.get("/parking_spots/", response_model=list[schemas.ParkingSpot])
def read_parking_spots(db: Session = Depends(get_db)):
    return crud.get_parking_spots(db=db)

@app.post("/vehicles/", response_model=schemas.Vehicle)
def create_vehicle(request:Request, vehicle: schemas.VehicleCreate, db: Session = Depends(get_db)):
    return crud.create_vehicle(request,db=db, vehicle=vehicle)

@app.get("/vehicles/", response_model=list[schemas.Vehicle])
def read_vehicles(request: Request, db: Session = Depends(get_db)):
    return crud.get_vehicles(request,db=db)

@app.put("/vehicles/{id}")
def edit_vehicle(request: Request, id: int, vehicle: schemas.VehicleCreate ,db: Session = Depends(get_db)):
    crud.update_vehicle(request, id=id, vehicle=vehicle ,db=db)
    return JSONResponse(status_code=200, content={"message": "Vehicle updated"})
@app.delete("/vehicles/{id}", response_model=list[schemas.Vehicle])
def delete_vehicle(request: Request, id: int, db: Session = Depends(get_db)):
    return crud.delete_vehicle(request, id=id, db=db)

@app.post("/parking_sessions/", response_model=schemas.ParkingSession)
def create_parking_session(session: schemas.ParkingSessionCreate, db: Session = Depends(get_db)):
    return crud.create_parking_session(db=db, session=session)
	