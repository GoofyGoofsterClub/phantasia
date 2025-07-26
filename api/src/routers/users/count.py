from fastapi import APIRouter
from src.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/count")
async def user_count():
    count = await User.all().count()
    return {"count": count}