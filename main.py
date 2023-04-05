import os

import openai
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import find_dotenv, load_dotenv

from keyboards import kb
from models import Numbers
from numbers_model import new_number

load_dotenv(find_dotenv())

# config
openai.api_key = str(os.getenv('CHATGPT_TOKEN'))
bot = Bot(str(os.getenv('BOT_TOKEN')))
dp = Dispatcher(bot)


class FSMSearch(StatesGroup):
    name = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    """
    Список команд и кнопки
    """
    await bot.send_message(
        message.chat.id, 
        'Выполнять команды строго по форме ниже:\n'
        '/chatgpt [text]\n'
        '/addnumber [last_name] [first_name] [patronymic] [number]',
        reply_markup=kb,
    )  


# numbers
@dp.message_handler(commands=['addnumber'])
async def add_number(message: types.Message):
    """
    Добавить новую запись в базу
    """
    result = new_number(message)
    if result:
        await bot.send_message(message.chat.id, 'Данные внесены')
    else:
        await bot.send_message(message.chat.id, 'Команда использована неверно')
    
    
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


@dp.message_handler(commands=['убратькнопки'])
async def delkb(message: types.Message):
    mk = types.ReplyKeyboardRemove()
    await bot.send_message(message.chat.id, 'ok', reply_markup=mk)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
