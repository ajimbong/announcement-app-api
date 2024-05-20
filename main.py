from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

# from . import crud, models, schemas
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/staffs/", response_model=schemas.Staff)
def create_staff(staff: schemas.StaffCreate, db: Session = Depends(get_db)):
    db_staff = crud.get_staff_by_email(db, email= staff.email)
    if db_staff:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_staff(db=db, staff=staff)


@app.get("/staffs/", response_model=list[schemas.Staff])
def read_staffs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    staffs = crud.get_staffs(db, skip=skip, limit=limit)
    return staffs


@app.get("/staffs/{staff_id}", response_model=schemas.Staff)
def read_staff(staff_id: int, db: Session = Depends(get_db)):
    db_staff = crud.get_staff(db, staff_id=staff_id)
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Staff Account not found")
    return db_staff


@app.post("/staffs/{user_id}/channels/", response_model=schemas.Channel)
def create_channel_with_staff_id(
    user_id: int, channel: schemas.ChannelCreate, db: Session = Depends(get_db)
):
    return crud.create_channel(db=db, channel=channel, staff_id=user_id)


@app.get("/channels/", response_model=list[schemas.Channel])
def read_channel(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    channels = crud.get_channels(db, skip=skip, limit=limit)
    return channels