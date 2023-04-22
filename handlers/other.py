import os

import openai
from aiogram import Dispatcher, types

from keyboards.other import kb_start, kr
from settings import OPEN_AI_TOKEN, bot

openai.api_key = OPEN_AI_TOKEN

messages = []


async def chatgpt_turbo(message: types.Message):
    message_text = message.text[1:]
    messages.append({'role': 'user', 'content': message_text})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    await message.answer(
        response['choices'][0]['message']['content'], 
        parse_mode="markdown",
    )
    

async def start(message: types.Message):
    """
    Список команд и кнопки
    """
    await bot.send_message(
        message.chat.id, 
        'Чтобы авторизоваться введите /auth '
        'или нажмите на соотвествующую кнопку'
        '\n\n\n'
        '/chatgpt [text]\n',
        reply_markup=kb_start,
    )
    

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


async def get_id(message: types.Message):
    """
    Команда чтобы получить id пользователя и чата
    """
    await bot.send_message(
        message.chat.id,
        f'chat: {message.chat.id}, user: {message.from_user.id}',
        reply_markup=kr,
    )


async def nocom(message: types.Message):
    await bot.send_message(message.chat.id, "Команда не существует", reply_markup=kb_start)
    await message.delete()


async def echo(message: types.Message):
    await bot.send_message(
        message.chat.id, 
        'Не понимаю о чем ты',
        reply_markup=kb_start,
    ) 
    await message.delete()


async def removekb(message: types.Message):
    """
    Удаляет кнопки
    """
    kr = types.ReplyKeyboardRemove()
    await bot.send_message(message.chat.id, 'ok', reply_markup=kr)


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(chatgpt_turbo, lambda message: message.text.startswith("\\"))
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(chatgpt, commands=['chatgpt'])
    dp.register_message_handler(get_id, commands=['id'])
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(removekb, commands=['removekb'])
    dp.register_message_handler(nocom, lambda message: message.text.startswith("/"))
    dp.register_message_handler(echo)
