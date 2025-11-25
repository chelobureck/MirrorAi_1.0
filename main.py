from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi.security import OAuth2PasswordBearer
import redis.asyncio as redis
from config.settings import get_settings
from models.database import Base, engine, init_db
from routers import (
    auth,
    boards
)

import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


settings = get_settings()
app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В production лучше указать конкретные домены
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)


app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["auth"])
app.include_router(boards.router, prefix=settings.API_V1_STR, tags=["boards"])
"""
тут надо прописать роутеры, в остальном баги исправлены, сервер запускается
"""

@app.get("/")
async def root():
    return {"message": "Welcome to SayDeck API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    return {"token": token}

@app.on_event("startup")
async def startup_event():
    try:
        # Инициализируем базу данных
        await init_db()
        print("✅ База данных успешно инициализирована!")
        
        # Инициализируем Redis для rate limiting
        # В Docker используем правильный URL для Redis
        redis_url = os.getenv("REDIS_URL", "redis://redis:6379")
        print(f"🔗 Подключение к Redis: {redis_url}")
        
        try:
            redis_client = redis.from_url(
                redis_url,
                encoding="utf-8",
                decode_responses=True
            )
            await FastAPILimiter.init(redis_client)
            print("✅ Redis успешно инициализирован!")
        except Exception as re:
            print(f"⚠️ Redis недоступен или не инициализирован: {re}")
            print("Продолжаем работу без ограничения частоты запросов")
    except Exception as e:
        print(f"❌ Ошибка при запуске приложения: {e}")
        # В production здесь можно добавить логирование и метрики
        raise