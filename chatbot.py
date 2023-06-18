import openai as openai

from api_message_structure import Prompt, Message, Conversation
from const import BOT_NAME, BOT_INSTRUCTIONS
from logger import Logger
from storage.local_storage import LocalStorage
from storage.objects.user import User


class ChatBot:
    def __init__(self, logger: Logger):
        self._bot_name = BOT_NAME
        self._instructions = BOT_INSTRUCTIONS

        self._logger: Logger = logger
        self.db = LocalStorage()

    def answer(self, user_id: int, message: str) -> str:
        self._logger.debug(f"User: {user_id} Message: {message}")
        user = self.db.get_user(user_id)
        user.add_message(message)

        return self._do_completion(user)

    def _do_completion(self, user: User) -> str:
        prompt = Prompt(
            header=Message("System",
                           f"Instructions for {self._bot_name}: {BOT_INSTRUCTIONS}"),
            convo=Conversation(
                [Message('user', m) for m in user.dialog] + [Message(self._bot_name)]
            )
        )
        prompt = prompt.render()

        completion = openai.Completion.create(
            engine=self._bot_name,
            prompt=prompt,
            temperature=0.7,
            top_p=0.7,
            max_tokens=512,
            stop=["<|endoftext|>"],
        )

        answer = completion['choices'][0]['text'].strip()
        if "->" in answer:
            answer = answer.split("->")[0].strip()
        return answer
