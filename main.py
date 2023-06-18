import telebot
import openai

import os

from chatbot import ChatBot
from logger import Logger

TG_BOT_KEY = os.environ['TG_BOT_KEY']
OPENAI_KEY = os.environ['OPENAI_KEY']

openai.api_key = OPENAI_KEY
bot = telebot.TeleBot(TG_BOT_KEY)

logger = Logger()
cb = ChatBot(
    logger=logger
)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(
        message,
        cb.answer(message.from_user.id, 'Привет. Кто ты такой?'),
    )


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(
        message,
        cb.answer(message.from_user.id, message.text),
    )


if __name__ == '__main__':
    logger.debug('Starting bot...')
    bot.polling()
    logger.debug('Bot closed.')
