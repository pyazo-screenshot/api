from fastapi import APIRouter, Depends, UploadFile, Response, status
from fastapi.params import File, Path

from pyazo_api.domain.auth.dto.user import UserGet
from pyazo_api.domain.auth.models.user import User
from pyazo_api.domain.images.actions.delete_image import DeleteImageAction
from pyazo_api.domain.images.actions.save_image import SaveImageAction
from pyazo_api.domain.images.dto.image import ImageGet
from pyazo_api.domain.images.repositories.image import ImageRepository
from pyazo_api.util.auth import get_current_user

router = APIRouter()


@router.post('/')
async def upload_image(
    upload_file: UploadFile = File(...),
    upload_action: SaveImageAction = Depends(SaveImageAction),
    authed_user: User = Depends(get_current_user)
):
    return upload_action(upload_file, UserGet(username=authed_user.username, id=authed_user.id))


@router.delete('/{image_id}')
async def delete_image(
    response: Response,
    image_id: int = Path(..., title="The ID of the image to delete"),
    authed_user: User = Depends(get_current_user),
    delete_image_action: DeleteImageAction = Depends(DeleteImageAction),
):
    delete_image_action(image_id)
    response.status_code = status.HTTP_204_NO_CONTENT


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
