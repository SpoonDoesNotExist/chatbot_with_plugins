from typing import List

from api_message_structure import Message


class User:
    def __init__(self, uid: str):
        self._id: str = uid
        self._dialog: List[Message] = []

    @property
    def id(self):
        return self._id

    @property
    def dialog(self):
        return self._dialog

    def add_user_message(self, message: str):
        self._dialog.append(Message('user', message))

    def add_bot_message(self, bot_name: str, message: str):
        self._dialog.append(Message(bot_name, message))
