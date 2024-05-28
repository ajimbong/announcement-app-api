from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import models
from .db.database import engine
from .routes import staff, channel, student, subscription

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Announcement Application",
    description="""
    # YOLO ✌️
    """,
    summary="Backend API for my Siantou App Project",
    version="0.0.1",
    contact={
        "name": "Ajim",
        "url": "https://ajim.dev",
        "email": "hello@ajim.dev",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(student.router)
app.include_router(staff.router)
app.include_router(channel.router)
app.include_router(subscription.router)


