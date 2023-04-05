import os

import openai
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import find_dotenv, load_dotenv

from keyboards import kbs, kbn
from numbers_model import set_number, get_numbers

load_dotenv(find_dotenv())

# config
openai.api_key = str(os.getenv('CHATGPT_TOKEN'))
storage = MemoryStorage()
bot = Bot(str(os.getenv('BOT_TOKEN')))
dp = Dispatcher(bot, storage=storage)


class FSMSearch(StatesGroup):
    field = State()
    value = State()


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
        '/addnumber [last_name] [first_name] [patronymic] [number]',
        reply_markup=kbs,
    )  


# numbers
@dp.message_handler(commands=['addnumber'])
async def add_number(message: types.Message):
    """
    Добавить новую запись в модель
    """
    result = set_number(message)
    if result:
        await bot.send_message(message.chat.id, 'Данные внесены')
    else:
        await bot.send_message(message.chat.id, 'Команда использована неверно')     


@dp.message_handler(state='*', commands="stop")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return None
    await state.finish()
    await message.reply("ok", reply_markup=kr)  
    

@dp.message_handler(commands=['number'], state=None)
async def number(message: types.Message):
    """
    Запрос на поиск по одному из полей в моделе
    """
    await FSMSearch.field.set()
    await bot.send_message(
        message.chat.id, 
        'По какому полю поиск?\nИспользовать только указанные кнопки\n'
        'Фамилия Имя Отчество соответственно',
        reply_markup=kbn,
    )


@dp.message_handler(state=FSMSearch.field)
async def field(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['field'] = message.text
        await FSMSearch.next()
        await bot.send_message(
            message.chat.id, 
            'Кого ищем?', 
            reply_markup=kr,
        )


@dp.message_handler(state=FSMSearch.value)
async def value(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['value'] = message.text
        response = get_numbers(data['field'], data['value'])
        if response:
            await bot.send_message(
                message.chat.id, 
                response,
                reply_markup=kbs,
            )
        else:
            await bot.send_message(
                message.chat.id, 
                'Записи не найдены или произошла ошибка, '
                'проверьте введенные данные',
                reply_markup=kbs,
            )
            
    await state.finish()


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
    """
    Удаляет кнопки
    """
    kr = types.ReplyKeyboardRemove()
    await bot.send_message(message.chat.id, 'ok', reply_markup=kr)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
