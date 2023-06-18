from typing import List


class User:
    def __init__(self, uid: str):
        self._id: str = uid
        self._dialog: List[str] = []

    @property
    def id(self):
        return self._id

    @property
    def dialog(self):
        return self._dialog

    def add_message(self, message: str):
        self._dialog.append(message)
