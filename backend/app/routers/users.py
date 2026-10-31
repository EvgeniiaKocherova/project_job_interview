from fastapi import APIRouter, Depends
from app.models import User
from app.dependencies import get_current_user
from app.schemas import UserResponse

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    # Если токен невалидный, сюда код даже не дойдет (выкинет 401 ошибку)
    return current_user