from io import BytesIO
from typing import Optional, Union

import openai as openai
import requests

from api_message_structure import Prompt, Message, Conversation
import const
from logger import Logger
from storage.local_storage import LocalStorage
from storage.objects.user import User


class ChatBot:
    def __init__(self, logger: Logger):
        self._bot_name = const.BOT_NAME
        self._instructions = const.BOT_INSTRUCTIONS

        self._logger: Logger = logger
        self.db = LocalStorage()

    async def generate(self, user_id: int, message: str) -> Optional[Union[BytesIO, None]]:
        user = self.db.get_user(user_id)
        user.add_user_message(message)

        response = await openai.Image.acreate(
            prompt=message,
            n=1,
            size="256x256"
        )
        image_url = response['data'][0]['url']
        return self._download_image(image_url)

    def _download_image(self, url) -> Optional[Union[BytesIO, None]]:
        try:
            response = requests.get(url)
            response.raise_for_status()
            image_data = BytesIO(response.content)
            return image_data
        except Exception as e:
            print('Error downloading image:', e)
            return None

    async def answer(self, user_id: int, message: str) -> str:
        self._logger.debug(f"User: {user_id} Message: {message}")
        user = self.db.get_user(user_id)

        bot_answer = await self._do_completion(user, message)
        user.add_user_message(message)
        user.add_bot_message(self._bot_name, bot_answer)
        return bot_answer

    async def _do_completion(self, user: User, message: str) -> str:
        prompt = self._get_prompt(user, message)
        print(f"Prompt: {prompt}")

        completion = await openai.Completion.acreate(
            engine=const.API_BOT_NAME,
            prompt=prompt,
            temperature=const.TEMPERATURE,
            top_p=const.TOP_P,
            max_tokens=const.MAX_TOKENS,
            stop=const.SEPARATOR_TOKEN,
        )

        answer = completion['choices'][0]['text'].strip()
        if "->" in answer:
            answer = answer.split("->")[0].strip()
        return answer

    def _get_prompt(self, user: User, message: str) -> str:
        conv_tail = [
            Message('user', 'Ответь на следующий вопрос:'),
            Message('user', message),
            Message(self._bot_name),
        ]
        prompt = Prompt(
            header=Message('System', const.BOT_INSTRUCTIONS),
            convo=Conversation(
                user.dialog + conv_tail
            )
        )
        return prompt.render()
