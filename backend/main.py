from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_db_and_tables
from app.routers import auth, users  # Импортируем оба роутера


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Запуск сервера. Создание таблиц в БД...")
    await create_db_and_tables()
    yield
    print("Остановка сервера.")

# 1. Сначала создаем приложение
app = FastAPI(
    title="Interview Platform API",
    lifespan=lifespan
)

# 2. Настраиваем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. И только теперь подключаем роутеры (app уже существует!)
app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "Бэкенд работает! База данных подключена."}