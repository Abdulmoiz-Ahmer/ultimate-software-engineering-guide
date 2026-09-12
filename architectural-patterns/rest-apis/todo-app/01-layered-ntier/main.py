from fastapi import FastAPI
from app.api.routes import router


app = FastAPI(title="Todo Using layered architecture", description="This is a sample todo application structured using layered architecture", version="1.0.0")

app.include_router(router)