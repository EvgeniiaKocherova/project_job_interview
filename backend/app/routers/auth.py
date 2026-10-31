from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.database import get_session
from app.models import User
from app.schemas import UserRegister, UserLogin, Token
from app.security import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, session: AsyncSession = Depends(get_session)):
    # 1. Проверяем, есть ли уже такой email
    statement = select(User).where(User.email == user_data.email)
    results = await session.exec(statement)
    existing_user = results.first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Пользователь с таким email уже существует"
        )
    
    # 2. Хешируем пароль и создаем пользователя
    hashed_pwd = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        name=user_data.name,
        password_hash=hashed_pwd
    )
    
    # 3. Сохраняем в БД
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    
    return {"message": "Пользователь успешно зарегистрирован", "user_id": new_user.id}


@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, session: AsyncSession = Depends(get_session)):
    # 1. Ищем пользователя
    statement = select(User).where(User.email == user_data.email)
    results = await session.exec(statement)
    user = results.first()
    
    # 2. Проверяем пароль
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль"
        )
    
    # 3. Создаем токен (в будущем добавим refresh_token)
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {"access_token": access_token, "token_type": "bearer"}