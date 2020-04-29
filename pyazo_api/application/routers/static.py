from fastapi import APIRouter, Depends

from pyazo_api.domain.auth.dto.user import UserGet
from pyazo_api.domain.auth.models.user import User
from pyazo_api.domain.images.actions.get_static import GetStaticAction
from pyazo_api.util.auth import get_current_user_or_none

router = APIRouter()


@router.get('/{image_id}', tags=["images"])
async def get_image(
        image_id: str,
        get_static_action: GetStaticAction = Depends(),
        authed_user: User = Depends(get_current_user_or_none),
):
    if authed_user is None:
        return get_static_action(image_id, None)

    return get_static_action(image_id, UserGet(id=authed_user.id, username=authed_user.username))
