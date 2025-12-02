from typing import Annotated

from fastapi import APIRouter, Depends, Path, Response, UploadFile, status

from pyazo_api.domain.auth.dto import User
from pyazo_api.domain.images.actions.delete_image import DeleteImageAction
from pyazo_api.domain.images.actions.get_images import GetImagesAction
from pyazo_api.domain.images.actions.save_image import SaveImageAction
from pyazo_api.domain.images.dto import Image
from pyazo_api.util.auth import get_current_user
from pyazo_api.util.pagination import (
    PaginatedResults,
    PaginationRequest,
    extract_pagination,
)

router = APIRouter()


@router.post("")
async def upload_image(
    upload_action: Annotated[SaveImageAction, Depends()],
    authed_user: Annotated[User, Depends(get_current_user)],
    upload_file: UploadFile,
    clear_metadata: bool = False,
) -> Image:
    return await upload_action(
        upload_file,
        clear_metadata,
        authed_user.to_public(),
    )


@router.delete("/{image_id}")
async def delete_image(
    response: Response,
    authed_user: Annotated[User, Depends(get_current_user)],
    delete_image_action: Annotated[DeleteImageAction, Depends()],
    image_id: Annotated[str, Path(title="The ID of the image to delete")],
) -> None:
    await delete_image_action(image_id, authed_user.to_public())
    response.status_code = status.HTTP_204_NO_CONTENT


@router.get("")
async def get_images(
    get_images_action: Annotated[GetImagesAction, Depends()],
    pagination: Annotated[PaginationRequest, Depends(extract_pagination)],
    authed_user: Annotated[User, Depends(get_current_user)],
) -> PaginatedResults:
    return await get_images_action(
        authed_user.to_public(),
        pagination,
    )
