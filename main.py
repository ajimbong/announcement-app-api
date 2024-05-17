from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

# from . import crud, models, schemas
from . import crud, models, schemas
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
    db_staff = crud.get_staff_by_email(db, emailstaffr.email)
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


# @app.post("/staffs/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/channels/", response_model=list[schemas.Channel])
def read_channel(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    channels = crud.get_channels(db, skip=skip, limit=limit)
    return channels


# from fastapi import FastAPI
# from typing import Optional
# from schemas import Staff

# app = FastAPI()

# @app.get('/')
# def get_staff(lim: int = 10, sort: Optional[str] = None):
#     return {
#         "message": [1,3,5,lim]
#     }

# @app.get('/{id}')
# def get_staff_by_id(id: int):
#     return {'data': id}


# @app.post('/')
# def create_staff(request: Staff):
#     return Staff