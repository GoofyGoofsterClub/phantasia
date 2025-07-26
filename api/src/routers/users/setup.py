from fastapi import APIRouter, Response, status
from src.models.user import User
from pydantic import BaseModel
from src.internal.error import ErrorDetails

router = APIRouter(prefix="/users", tags=["Users"])

class SuperuserSetupRespnnse(BaseModel):
    access_key: str

@router.get("/setup",
    summary="This endpoint is only for initial setup",
    description="This endpoint is only for initial setup and will not be usable afterwards",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": SuperuserSetupRespnnse},
        status.HTTP_418_IM_A_TEAPOT: {"model": ErrorDetails}
    })
async def user_setup(response: Response):
    user_count = await User.all().count()

    if user_count == 0:
        user = await User.create_with_token(username="admin", permissions=["USER_ALL", "SUPERUSER"])
        return SuperuserSetupRespnnse(access_key=user[1])
    else:
        response.status_code = status.HTTP_418_IM_A_TEAPOT
        return ErrorDetails(error="Nothing to see here", status_code=status.HTTP_418_IM_A_TEAPOT)