import os

import openai

from aiogram import Bot, Dispatcher, executor, types

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

openai.api_key = os.getenv("CHATGPT_TOKEN")
bot = Bot(os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)


kb = [
    [types.KeyboardButton(text="/start")],
]
keyboard = types.ReplyKeyboardMarkup(
    keyboard=kb,
    resize_keyboard=True,
    input_field_placeholder="Че хочешь?!",
)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Пиши /chatgpt и что тебе нужно")  
    
    
@dp.message_handler(commands=['chatgpt'])
async def send(message: types.Message):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message.text,
        temperature=0.9,
        max_tokens=2000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.6,
    )
    await message.answer(response['choices'][0]['text'])
    

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
