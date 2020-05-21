from fastapi import APIRouter, Depends, UploadFile, Response, status
from fastapi.params import File, Path

from pyazo_api.domain.auth.dto.user import UserGet
from pyazo_api.domain.auth.models.user import User
from pyazo_api.domain.images.actions.delete_image import DeleteImageAction
from pyazo_api.domain.images.actions.save_image import SaveImageAction
from pyazo_api.domain.images.actions.create_thumbnail import CreateThumbnailAction
from pyazo_api.domain.images.actions.get_images import GetImagesAction
from pyazo_api.domain.images.dto.image import ImageBaseResource
from pyazo_api.util.pagination import Pagination, extract_pagination
from pyazo_api.util.auth import get_current_user

router = APIRouter()


@router.post('', tags=["images"])
async def upload_image(
    upload_file: UploadFile = File(...),
    private: bool = False,
    clear_metadata: bool = False,
    upload_action: SaveImageAction = Depends(),
    authed_user: User = Depends(get_current_user),
):
    return upload_action(
        upload_file,
        private,
        clear_metadata,
        UserGet(username=authed_user.username, id=authed_user.id)
    )


@router.delete('/{image_id}', tags=["images"])
async def delete_image(
    response: Response,
    image_id: str = Path(..., title="The ID of the image to delete"),
    authed_user: User = Depends(get_current_user),
    delete_image_action: DeleteImageAction = Depends(DeleteImageAction),
):
    delete_image_action(image_id, UserGet(username=authed_user.username, id=authed_user.id))
    response.status_code = status.HTTP_204_NO_CONTENT


@router.get('', tags=["images"])
async def get_images(
    pagination: Pagination = Depends(extract_pagination),
    authed_user: User = Depends(get_current_user),
    get_images_action: GetImagesAction = Depends()
):
    return ImageBaseResource.paginated_collection(
        get_images_action(UserGet(username=authed_user.username, id=authed_user.id), pagination)
    )
