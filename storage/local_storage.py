from storage.base_storage import BaseStorage
from storage.objects.user import User


class LocalStorage(BaseStorage):
    def __init__(self):
        self.users = {}

    def get_user(self, user_id) -> User:
        return self.users.setdefault(
            user_id,
            User(
                uid=user_id,
            )
        )
