from fastapi import APIRouter, Depends, UploadFile, Response, status
from fastapi.params import File, Path

from pyazo_api.domain.auth.dto.user import UserGet
from pyazo_api.domain.auth.dto.user import User as UserDTO
from pyazo_api.domain.auth.models.user import User
from pyazo_api.domain.images.actions.delete_image import DeleteImageAction
from pyazo_api.domain.images.actions.delete_share import DeleteShareAction
from pyazo_api.domain.images.actions.save_image import SaveImageAction
from pyazo_api.domain.images.actions.share_image import ShareImageAction
from pyazo_api.domain.images.dto.image import ImageGet
from pyazo_api.domain.images.repositories.image import ImageRepository
from pyazo_api.domain.images.repositories.share import ShareRepository
from pyazo_api.util.auth import get_current_user

router = APIRouter()


@router.post('')
async def upload_image(
    upload_file: UploadFile = File(...),
    private: bool = False,
    clear_metadata: bool = False,
    upload_action: SaveImageAction = Depends(),
    authed_user: User = Depends(get_current_user)
):
    return upload_action(upload_file, private, clear_metadata, UserGet(username=authed_user.username, id=authed_user.id))


@router.delete('/{image_id}')
async def delete_image(
    response: Response,
    image_id: str = Path(..., title="The ID of the image to delete"),
    authed_user: User = Depends(get_current_user),
    delete_image_action: DeleteImageAction = Depends(DeleteImageAction),
):
    delete_image_action(image_id, UserGet(username=authed_user.username, id=authed_user.id))
    response.status_code = status.HTTP_204_NO_CONTENT


@router.get('')
async def get_images(
    authed_user: User = Depends(get_current_user),
    image_repository: ImageRepository = Depends(ImageRepository)
):
    return [
        ImageGet(
            id=image.id,
            owner_id=image.owner_id,
            private=image.private
        )
        for image in image_repository.get_all_by_user_id(authed_user.id)
    ]


@router.post('/{image_id}/shares')
async def share_image(
    image_id: str,
    user: UserDTO,
    share_action: ShareImageAction = Depends(),
    authed_user: User = Depends(get_current_user)
):
    return share_action(image_id, user, UserGet(username=authed_user.username, id=authed_user.id))


@router.delete('/shares/{share_id}')
async def delete_share(
    response: Response,
    share_id: str,
    authed_user: User = Depends(get_current_user),
    delete_share_action: DeleteShareAction = Depends(),
):
    delete_share_action(share_id, UserGet(username=authed_user.username, id=authed_user.id))
    response.status_code = status.HTTP_204_NO_CONTENT


@router.get('/shares')
async def get_shares(
    authed_user: User = Depends(get_current_user),
    share_repository: ShareRepository = Depends()
):
    return [
        ImageGet(
            id=share.image.id,
            owner_id=share.image.owner_id,
            private=share.image.private
        )
        for share in share_repository.get_all_shares_by_user_id(authed_user.id)
    ]
