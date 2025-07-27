from fastapi import APIRouter, Response, status, File, UploadFile, Request
from pydantic import BaseModel
from typing import List

from src.models.user import User
from src.models.upload import Upload
from src.internal.authmgr import requires_auth
from src.internal.error import ErrorDetails
from src.utils.random import generate_random_string
from src.internal.permissions import UserPermissions

router = APIRouter(prefix="/uploads", tags=["Uploads"])

class NewUploadCreated(BaseModel):
    direct_link: str
    visual_link: str

@router.post("/create", status_code=201,
            summary="Uploads a new file",
            description="Uploads a new file",
            responses={
                status.HTTP_201_CREATED: {"model": NewUploadCreated},
                status.HTTP_400_BAD_REQUEST: {"model": ErrorDetails}
            })
@requires_auth(permissions_required=[UserPermissions.USER_UPLOAD])
async def create_new_upload(request: Request, file: UploadFile, response: Response, *,
    user: User):
    s3 = request.app.state.s3_client
    s3_bucket = request.app.state.s3_bucket
    s3_domain = request.app.state.s3_domain

    internal_name = f"{user.username}/{generate_random_string(16)}.{file.filename.split('.')[-1]}"
    s3.upload_fileobj(file.file, s3_bucket, internal_name, ExtraArgs={"ACL": "public-read"})

    direct_link = f"https://{s3_domain}/{internal_name}"
    visual_link = f"https://{request.headers.get('X-Base-Host', s3_domain)}/{user.username[:2]}{generate_random_string(9)}"

    await Upload.create(
        user=user,
        filename=file.filename,
        visual_name=visual_link.split('/')[-1],
        mimetype=file.content_type,
        file_hash=internal_name.split('/')[-1].split('.')[0],
        internal_name=internal_name,
        filesize=file.size
    )

    user.upload_count += 1
    await user.save()
    
    response.status_code = status.HTTP_201_CREATED
    return {"direct_link": direct_link, "visual_link": visual_link}

