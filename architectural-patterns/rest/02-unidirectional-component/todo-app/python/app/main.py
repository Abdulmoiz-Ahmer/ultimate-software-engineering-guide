from fastapi import FastAPI
from app.components.todos.router import router as todo_router

app = FastAPI(
    title="Todo Using Unidirectional Component Architecture",
    description="This is a sample todo application structured using unidirectional component architecture",
    version="1.0.0",
)

app.include_router(todo_router)
