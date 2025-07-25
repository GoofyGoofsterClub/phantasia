from fastapi import APIRouter
from src.models.user import User

router = APIRouter(prefix="/users/count", tags=["Users"])

@router.get("/")
async def user_count():
    count = await User.all().count()
    return {"count": count}