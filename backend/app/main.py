from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routes.dashboard import router as dashboard_router
from app.routes.documents import router as documents_router
from app.routes.learning import router as learning_router
from app.routes.quiz import router as quiz_router
from app.routes.auth import router as auth_router
from app.routes.course import router as course_router
from app.routes.enrollment import router as enrollment_router
from app.routes.profile import router as profile_router
from app.routes.lesson import router as lesson_router
from app.routes.course_progress import router as course_progress_router
from app.routes import lesson_completion
from app.routes import users

from app.database.mongodb import (
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
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router)
app.include_router(course_router)
app.include_router(dashboard_router)
app.include_router(documents_router)
app.include_router(learning_router)
app.include_router(quiz_router)
app.include_router(enrollment_router)
app.include_router(profile_router)
app.include_router(lesson_router)
app.include_router(course_progress_router)
app.include_router(lesson_completion.router)
app.include_router(users.router)


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