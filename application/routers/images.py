from fastapi import APIRouter, Depends, UploadFile
from fastapi.params import File

from domain.auth.dto.user import UserGet
from domain.auth.models.user import User
from domain.images.actions.save_image import SaveImageAction
from domain.images.dto.image import ImageGet
from domain.images.repositories.image import ImageRepository
from util.auth import get_current_user

router = APIRouter()


@router.post('/')
async def upload_image(
    upload_file: UploadFile = File(...),
    upload_action: SaveImageAction = Depends(SaveImageAction),
    authed_user: User = Depends(get_current_user)
):
    return upload_action(upload_file, UserGet(username=authed_user.username, id=authed_user.id))


@router.get('/')
async def get_images(
    authed_user: User = Depends(get_current_user),
    image_repository: ImageRepository = Depends(ImageRepository)
):
    return [
        ImageGet(
            id=image.id,
            owner_id=image.owner_id,
            path=image.path
        )
        for image in image_repository.get_all_by_user_id(authed_user.id)
    ]
