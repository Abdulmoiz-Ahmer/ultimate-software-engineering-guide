from fastapi import FastAPI
from app.views.todo_view import router as todo_router

app = FastAPI(
    title="MVVM Architecture Todo API",
    description="A REST API applying Model-View-ViewModel principles with FastAPI and SQLAlchemy",
    version="1.0.0",
)

app.include_router(todo_router)