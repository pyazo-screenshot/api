from fastapi import APIRouter, Depends

from pyazo_api.domain.auth.dto.user import UserGet
from pyazo_api.domain.auth.models.user import User
from pyazo_api.domain.static.actions.get_static import GetStaticAction
from pyazo_api.util.auth import get_current_user_or_none, get_current_user

router = APIRouter()


@router.get('/{image_path}')
async def static(
        image_path: str,
        get_static_action: GetStaticAction = Depends(),
        authed_user: User = Depends(get_current_user_or_none),
):
    if authed_user is None:
        return get_static_action(image_path, None)

    return get_static_action(image_path, UserGet(id=authed_user.id, username=authed_user.username))
