from io import BytesIO

import openai as openai
import requests

from api_message_structure import Prompt, Message, Conversation
from const import BOT_NAME, BOT_INSTRUCTIONS, API_BOT_NAME
from logger import Logger
from storage.local_storage import LocalStorage
from storage.objects.user import User


class ChatBot:
    def __init__(self, logger: Logger):
        self._bot_name = BOT_NAME
        self._instructions = BOT_INSTRUCTIONS

        self._logger: Logger = logger
        self.db = LocalStorage()

    def generate(self, user_id: int, message: str):
        user = self.db.get_user(user_id)
        user.add_user_message(message)

        response = openai.Image.create(
            prompt=message,
            n=1,
            size="256x256"
        )
        image_url = response['data'][0]['url']
        return self._download_image(image_url)

    def _download_image(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            image_data = BytesIO(response.content)
            return image_data
        except Exception as e:
            print('Error downloading image:', e)
            return None

    def answer(self, user_id: int, message: str) -> str:
        self._logger.debug(f"User: {user_id} Message: {message}")
        user = self.db.get_user(user_id)

        bot_answer = self._do_completion(user, message)
        user.add_user_message(message)
        user.add_bot_message(self._bot_name, bot_answer)
        return bot_answer

    def _do_completion(self, user: User, message: str) -> str:
        prompt = self._get_prompt(user, message)
        print(f"Prompt: {prompt}")

        completion = openai.Completion.create(
            engine=API_BOT_NAME,
            prompt=prompt,
            temperature=0.92,
            top_p=0.9,
            max_tokens=512,
            stop='<|endoftext|>',
        )

        answer = completion['choices'][0]['text'].strip()
        if "->" in answer:
            answer = answer.split("->")[0].strip()
        return answer

    def _get_prompt(self, user: User, message: str):
        conv_tail = [
            Message('user', 'Ответь на следующий вопрос:'),
            Message('user', message),
            Message(self._bot_name),
        ]
        prompt = Prompt(
            header=Message('System', BOT_INSTRUCTIONS),
            convo=Conversation(
                user.dialog + conv_tail
            )
        )
        return prompt.render()
