from fastapi import APIRouter, Response, status, Header
from src.models.user import User
from pydantic import BaseModel
from typing import List, Annotated
from src.internal.error import ErrorDetails
from src.internal.success import SuccessMessage
from src.internal.authmgr import requires_auth

router = APIRouter(prefix="/users", tags=["Users"])

self_inflicted_allowed = ["username"]

prohibited_change = ["permissions", "badges"]

@router.get("/modify", status_code=200, response_model=None)
@requires_auth()
async def modify_user(target: str | None, field: str, value: str | int | bool, response: Response, *,
    user: User):
    if not target:
       target = user.username
    
    if target != user.username and not user.has_permission("MODIFY_OTHER_USERS"):
        response.status_code = status.HTTP_403_FORBIDDEN
        return ErrorDetails(error="You do not have permission to modify other users", status_code=status.HTTP_403_FORBIDDEN)
    
    if field in prohibited_change:
        response.status_code = status.HTTP_403_FORBIDDEN
        return ErrorDetails(error=f"You cannot modify field {field}", status_code=status.HTTP_403_FORBIDDEN)
    
    if field not in self_inflicted_allowed and target == user.username:
        response.status_code = status.HTTP_403_FORBIDDEN
        return ErrorDetails(error=f"You cannot modify your own {field}", status_code=status.HTTP_403_FORBIDDEN)
    
    if not hasattr(User, field):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorDetails(error=f"Invalid field {field}", status_code=status.HTTP_400_BAD_REQUEST)

    await User.filter(username=target).update(**{field: value})

    return SuccessMessage(success=True)