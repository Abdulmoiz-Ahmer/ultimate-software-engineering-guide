from fastapi import FastAPI
from app.frameworks_and_drivers.web.routes import router as todo_router

app = FastAPI(
    title="Uncle Bob Clean Architecture Todo API",
    description="Decoupled application built with FastAPI, SQLAlchemy, and SQLite",
    version="1.0.0",
)

app.include_router(todo_router)
