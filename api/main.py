from fastapi import Depends, FastAPI

from .db import models
from .db.database import engine
from .dependencies import get_db
from .routes import staff, channel

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(staff.router)
app.include_router(channel.router)

