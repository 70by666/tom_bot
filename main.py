import os

import openai
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())

# config
openai.api_key = str(os.getenv('CHATGPT_TOKEN'))

storage = MemoryStorage()

bot = Bot(str(os.getenv('BOT_TOKEN')))

dp = Dispatcher(bot, storage=storage)
    
    
kr = types.ReplyKeyboardRemove()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    """
    Список команд и кнопки
    """
    await bot.send_message(
        message.chat.id, 
        'Выполнять команды только по форме ниже:\n'
        '/chatgpt [text]\n'
    )  
    

@dp.message_handler(commands=['chatgpt'])
async def chatgpt(message: types.Message):
    """
    API open ai chatgpt
    """
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=message.text,
        temperature=0.9,
        max_tokens=2000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.6,
    )
    await bot.send_message(message.chat.id, response['choices'][0]['text'])


@dp.message_handler(commands=['id'])
async def send(message: types.Message):
    """
    Команда чтобы получить id пользователя и чата
    """
    await bot.send_message(
        message.chat.id,
        f'chat: {message.chat.id}, user: {message.from_user.id}',
    )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
