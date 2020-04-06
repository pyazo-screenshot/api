from fastapi.params import Depends

from pyazo_api.domain.images.exceptions.image import ImageNotFoundException
from pyazo_api.domain.images.repositories.image import ImageRepository
from pyazo_api.domain.images.repositories.share import ShareRepository
from pyazo_api.domain.auth.dto.user import UserGet
from starlette.responses import FileResponse


class GetStaticAction:
    def __init__(
            self,
            image_repository: ImageRepository = Depends(ImageRepository),
            share_repository: ShareRepository = Depends()
    ):
        self.image_repository = image_repository
        self.share_repository = share_repository

    def __call__(self, image_id: str, current_user: UserGet):
        image = self.image_repository.find_by_id(image_id)
        if not image:
            raise ImageNotFoundException

        if image.private:
            if not current_user:
                raise ImageNotFoundException

            if image.owner_id != current_user.id:
                share = self.share_repository.get_by_user_id_and_image_id(current_user.id, image.id)
                if not share:
                    raise ImageNotFoundException

        return FileResponse(f"public/images/{image_id}", media_type="image/png")
