from fastapi import Depends, FastAPI

from .db import models
from .db.database import engine
from .routes import staff, channel, student

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(staff.router)
app.include_router(channel.router)
app.include_router(student.router)

