import os

import openai
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import find_dotenv, load_dotenv

from keyboards import kbs, kbn, kba
from numbers_model import set_number, get_numbers

load_dotenv(find_dotenv())

# config
openai.api_key = str(os.getenv('CHATGPT_TOKEN'))

storage = MemoryStorage()

bot = Bot(str(os.getenv('BOT_TOKEN')))

dp = Dispatcher(bot, storage=storage)

whitelist = str(os.getenv('WHITELIST')).split()


class FSMSearch(StatesGroup):
    field = State()
    value = State()


class FSMNewNumber(StatesGroup):
    last_name = State()
    first_name = State()
    patronymic = State()
    number = State()
    

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
        reply_markup=kbs,
    )  


@dp.message_handler(state='*', commands="stop")
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Отмена машины состояний
    """
    current_state = await state.get_state()
    if current_state is None:
        return None
    await state.finish()
    await message.reply("ok", reply_markup=kbs)  


# numbers

# add_number

@dp.message_handler(commands=['addnumber'], state=None)
async def add_number(message: types.Message):
    """
    Добавить новую запись в модель, ждет фамилию
    """
    if str(message.from_user.id) in whitelist:
        await FSMNewNumber.last_name.set()
        await bot.send_message(
            message.chat.id, 
            'Введите фамилию',
            reply_markup=kba,
        )
    else:
        await bot.send_message(
            message.chat.id, 
            'Нет доступа', 
            reply_markup=kbs,
        )


@dp.message_handler(state=FSMNewNumber.last_name)
async def field(message: types.Message, state: FSMContext):
    """
    Записывает фамилию и ждет имя
    """
    async with state.proxy() as data:
        data['last_name'] = message.text
        await FSMNewNumber.next()
        await bot.send_message(
            message.chat.id, 
            'Введите имя', 
            reply_markup=kr,
        )     


@dp.message_handler(state=FSMNewNumber.first_name)
async def field(message: types.Message, state: FSMContext):
    """
    Записывает имя и ждет отчество
    """
    async with state.proxy() as data:
        data['first_name'] = message.text
        await FSMNewNumber.next()
        await bot.send_message(
            message.chat.id, 
            'Введите отчество', 
            reply_markup=kr,
        )   
        
        
@dp.message_handler(state=FSMNewNumber.patronymic)
async def field(message: types.Message, state: FSMContext):
    """
    Записывает отчество и ждет номер
    """
    async with state.proxy() as data:
        data['patronymic'] = message.text
        await FSMNewNumber.next()
        await bot.send_message(
            message.chat.id, 
            'Введите номер', 
            reply_markup=kr,
        )   
      
  
@dp.message_handler(state=FSMNewNumber.number)
async def field(message: types.Message, state: FSMContext):
    """
    Записывает номер и закрывает машину состояний, создает запись в моделе
    """
    async with state.proxy() as data:
        data['number'] = message.text
        result = set_number(
            message.from_user, 
            data['last_name'], 
            data['first_name'], 
            data['patronymic'], 
            data['number'],
        )
        if result:
            await bot.send_message(
                message.chat.id, 
                'Данные внесены',
                reply_markup=kbs,
            )
        else:
            await bot.send_message(
                message.chat.id, 
                'Команда использована неверно',
                reply_markup=kbs,
            )
        
    await state.finish()   
    

# get_number

@dp.message_handler(commands=['number'], state=None)
async def get_number(message: types.Message):
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
    """
    Записывает поле и далее ждет ключевое слово
    """
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
    """
    Записывает ключевое слово и выдает результат если он есть
    """
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


# chatgpt

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


# other

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
