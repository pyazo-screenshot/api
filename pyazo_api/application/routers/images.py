from typing import Any

from fastapi import APIRouter, Depends, File, Path, Response, UploadFile, status

from pyazo_api.domain.auth.dto import User, UserGet
from pyazo_api.domain.images.actions.delete_image import DeleteImageAction
from pyazo_api.domain.images.actions.save_image import SaveImageAction
from pyazo_api.domain.images.actions.get_images import GetImagesAction
from pyazo_api.util.pagination import PaginatedResults, PaginationRequest, extract_pagination
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
    return await upload_action(
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
    await delete_image_action(image_id, UserGet(username=authed_user.username, id=authed_user.id))
    response.status_code = status.HTTP_204_NO_CONTENT


@router.get('', tags=["images"])
async def get_images(
    get_images_action: GetImagesAction = Depends(),
    pagination: PaginationRequest = Depends(extract_pagination),
    authed_user: User = Depends(get_current_user),
) -> PaginatedResults:
    return await get_images_action(
        UserGet(username=authed_user.username, id=authed_user.id),
        pagination,
    )
