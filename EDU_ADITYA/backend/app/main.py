from fastapi import FastAPI
from contextlib import asynccontextmanager

from Eduverse.backend.app.routes.auth import router as auth_router
from Eduverse.backend.app.routes.course import router as course_router

from Eduverse.backend.app.database.mongodb import (
    connect_to_mongo,
    close_mongo_connection
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()

    yield

    await close_mongo_connection()


app = FastAPI(
    title="AI Learning Platform API",
    version="1.0.0",
    lifespan=lifespan
)


# Authentication routes
# app.include_router(auth_router)
app.include_router(auth_router)
app.include_router(course_router)

@app.get("/")
def home():
    return {
        "message": "AI Learning Platform Backend Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }