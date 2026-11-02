from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from pydantic import BaseModel, EmailStr
from jose import jwt, JWTError

from app.database import get_session
from app.models import User
from app.schemas import UserRegister, UserLogin, Token
from app.security import (
    get_password_hash, 
    verify_password, 
    create_access_token, 
    create_reset_token, 
    SECRET_KEY, 
    ALGORITHM
)
from app.mailer import send_reset_password_email

# 1. Создаем роутер
router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# --- Модели для валидации ---
class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordData(BaseModel):
    token: str
    new_password: str

# --- Эндпоинты ---

@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, session: AsyncSession = Depends(get_session)):
    # Проверяем, есть ли уже такой email
    statement = select(User).where(User.email == user_data.email)
    results = await session.exec(statement)
    existing_user = results.first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Пользователь с таким email уже существует"
        )
    
    # Хешируем пароль и создаем пользователя
    hashed_pwd = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        name=user_data.name,
        password_hash=hashed_pwd
    )
    
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    
    return {"message": "Пользователь успешно зарегистрирован", "user_id": new_user.id}


@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, session: AsyncSession = Depends(get_session)):
    # Ищем пользователя
    statement = select(User).where(User.email == user_data.email)
    results = await session.exec(statement)
    user = results.first()
    
    # Проверяем пароль
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль"
        )
    
    # Создаем токен
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout():
    return {"message": "Вы успешно вышли из системы"}


@router.post("/forgot-password")
async def forgot_password(data: ForgotPasswordRequest, session: AsyncSession = Depends(get_session)):
    statement = select(User).where(User.email == data.email)
    results = await session.exec(statement)
    user = results.first()
    
    if user:
        # Генерируем токен и отправляем письмо
        token = create_reset_token(user.email)
        await send_reset_password_email(user.email, token)
        
    # Всегда возвращаем 200, чтобы не раскрывать базу
    return {"message": "Если такой email существует, письмо с инструкцией отправлено."}


@router.post("/reset-password")
async def reset_password(data: ResetPasswordData, session: AsyncSession = Depends(get_session)):
    try:
        # Расшифровываем токен
        payload = jwt.decode(data.token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        token_type = payload.get("type")
        
        if email is None or token_type != "reset":
            raise HTTPException(status_code=400, detail="Неверный токен")
            
    except JWTError:
        raise HTTPException(status_code=400, detail="Токен истек или неверен")
        
    statement = select(User).where(User.email == email)
    results = await session.exec(statement)
    user = results.first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
        
    # Хешируем и сохраняем новый пароль
    user.password_hash = get_password_hash(data.new_password)
    session.add(user)
    await session.commit()
    
    return {"message": "Пароль успешно изменен"}