from fastapi import APIRouter, Depends, Response, status

from pyazo_api.domain.auth.dto.user import UserGet
from pyazo_api.domain.auth.models.user import User
from pyazo_api.domain.images.actions.delete_share import DeleteShareAction
from pyazo_api.domain.images.actions.share_image import ShareImageAction
from pyazo_api.domain.images.actions.get_shares import GetSharesAction
from pyazo_api.domain.images.dto.share import ShareAdd, ShareGet
from pyazo_api.util.pagination import Pagination, extract_pagination
from pyazo_api.util.auth import get_current_user

router = APIRouter()


@router.post('', tags=["shares"])
async def share_image(
    share_data: ShareAdd,
    share_action: ShareImageAction = Depends(),
    authed_user: User = Depends(get_current_user)
):
    return ShareGet.make(share_action(share_data, UserGet(username=authed_user.username, id=authed_user.id)))


@router.delete('/{share_id}', tags=["shares"])
async def delete_share(
    response: Response,
    share_id: int,
    authed_user: User = Depends(get_current_user),
    delete_share_action: DeleteShareAction = Depends(),
):
    delete_share_action(share_id, UserGet(username=authed_user.username, id=authed_user.id))
    response.status_code = status.HTTP_204_NO_CONTENT


@router.get('', tags=["shares"])
async def get_shares(
    pagination: Pagination = Depends(extract_pagination),
    authed_user: User = Depends(get_current_user),
    get_shares_action: GetSharesAction = Depends()
):
    # TODO      N + 1 Problem
    return ShareGet.paginated_collection(
        get_shares_action(UserGet(username=authed_user.username, id=authed_user.id), pagination)
    )
