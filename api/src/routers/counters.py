from fastapi import APIRouter

router = APIRouter(prefix="/counters", tags=["Internal"])

@router.get("/")
async def counters():
    return []
