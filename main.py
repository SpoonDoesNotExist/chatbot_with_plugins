from aiogram import executor, Bot, Dispatcher, types
import openai

import os

import const
from chatbot import ChatBot
from logger import Logger

TG_BOT_KEY = os.environ['TG_BOT_KEY']
OPENAI_KEY = os.environ['OPENAI_KEY']

openai.api_key = OPENAI_KEY

bot = Bot(token=TG_BOT_KEY)
dp = Dispatcher(bot)

logger = Logger()
cb = ChatBot(logger=logger)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer(const.BOT_HELLO_MESSAGE)


@dp.message_handler(commands=['generate'])
async def generate(message: types.Message):
    text = message.text.replace('/generate', '').strip()
    image_data = await cb.generate(message.from_user.id, text)

    if image_data is None:
        await message.answer('Не получилось сгенерировать изображение.')
    await bot.send_photo(
        message.chat.id,
        photo=image_data,
    )


@dp.message_handler()
async def echo_all(message: types.Message):
    await message.answer(
        await cb.answer(message.from_user.id, message.text),
    )


if __name__ == '__main__':
    logger.debug('Starting bot...')
    executor.start_polling(dp, skip_updates=True)
    logger.debug('Bot closed.')
