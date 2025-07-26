from fastapi import APIRouter, Response, status
from src.models.user import User
from pydantic import BaseModel
from typing import List, Annotated, Optional
from src.internal.error import ErrorDetails
from src.internal.authmgr import requires_auth

router = APIRouter(prefix="/users", tags=["Users"])

class UserDetails(BaseModel):
    username: str
    created_at: str
    badges: List[str]
    is_banned: bool
    views: int
    upload_count: int

@router.get("/get", status_code=200, response_model=None)
@requires_auth()
async def get_user(target: Optional[str], response: Response, *,
    user: User):
    if not target:
       target = user.username
    
    if not await User.exists_by_username(target):
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorDetails(error=f"User does not exist", status_code=status.HTTP_404_NOT_FOUND)

    user_data = await User.find_by_username(target)
    return UserDetails(
        username=user_data.username,
        created_at=user_data.created_at.isoformat(),
        badges=user_data.badges,
        is_banned=user_data.is_banned,
        views=user_data.views,
        upload_count=user_data.upload_count
    )
