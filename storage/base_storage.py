from abc import ABC, abstractmethod


class BaseStorage(ABC):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    @abstractmethod
    def get_user(self, user_id):
        pass
