from pyazo_api.domain.auth.models.user import User
from pyazo_api.util.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.model = User
