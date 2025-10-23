from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import create_tables
from app.routers.auth.auth_router import router as auth_router
from app.routers.users.users_router import router as user_router
from app.routers.subscriptions.subscriptions_router import router as subscription_router
from app.routers.user_exercises.user_exercises_router import (
    router as user_exercise_router,
)
from app.routers.all_exercises.all_exercises_router import (
    router as all_exercises_router,
)
from app.routers.sets.sets_router import router as set_router

from app.exceptions.exceptions_handlers import register_exception_handlers
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_tables()
    yield
    # Shutdown (if needed)



app = FastAPI(lifespan=lifespan,debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 👈 Your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(subscription_router)
app.include_router(user_exercise_router)
app.include_router(all_exercises_router)
app.include_router(set_router)

register_exception_handlers(app)

