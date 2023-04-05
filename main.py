import os

import openai
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from dotenv import find_dotenv, load_dotenv

from keyboards import kba, kbn, kbs
from numbers_model import edit_number, get_number, get_numbers, set_number

load_dotenv(find_dotenv())

# config
openai.api_key = str(os.getenv('CHATGPT_TOKEN'))

storage = MemoryStorage()

bot = Bot(str(os.getenv('BOT_TOKEN')))

dp = Dispatcher(bot, storage=storage)

whitelist = str(os.getenv('WHITELIST')).split()

cd = CallbackData('dun_w', 'action', 'num_id')


class FSMSearch(StatesGroup):
    field = State()
    value = State()


class FSMNewNumber(StatesGroup):
    last_name = State()
    first_name = State()
    patronymic = State()
    number = State()


class FSMEdit(StatesGroup):
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
        '/chatgpt [text]\n',
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
    if not str(message.from_user.id) in whitelist:
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
            data,
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
    

# get_numbers

@dp.message_handler(commands=['number'], state=None)
async def get_numbers_from_fio(message: types.Message):
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
            reply_markup=kba,
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


# edit_number
@dp.message_handler(commands=['getnumber'])
async def get_number_from_id(message: types.Message):
    """
    Получить запись по id
    """
    if not str(message.from_user.id) in whitelist:
        try:
            response = get_number(message.text.split(' ')[1])
            if response:
                kbi = InlineKeyboardMarkup(row_width=2).add(
                    InlineKeyboardButton('Фамилию', callback_data=cd.new(
                        action='last_name',
                        num_id=response.id,
                    )),
                    InlineKeyboardButton('Имя', callback_data=cd.new(
                        action='first_name',
                        num_id=response.id,
                    )),
                    InlineKeyboardButton('Отчество', callback_data=cd.new(
                        action='patronymic',
                        num_id=response.id,
                    )),
                    InlineKeyboardButton('Номер', callback_data=cd.new(
                        action='number',
                        num_id=response.id,
                    )),
                    InlineKeyboardButton('Удалить', callback_data=cd.new(
                        action='delete',
                        num_id=response.id,
                    )),
                )
                text_message = '{} {} {} {} {}\n\nИзменить:'.format(
                    response.id,
                    response.last_name,
                    response.first_name,
                    response.patronymic,
                    response.number,
                )
                await bot.send_message(
                    message.chat.id, 
                    text_message,
                    reply_markup=kbi,
                )
            else:
                await bot.send_message(
                    message.chat.id, 
                    'Запись с таким ID не найдена',
                    reply_markup=kbs,
                )
        except IndexError:
            await bot.send_message(
                message.chat.id, 
                'Вы не указали ID',
                reply_markup=kbs,
            )
    else:
        await bot.send_message(
            message.chat.id, 
            'Нет доступа', 
            reply_markup=kbs,
        )


@dp.callback_query_handler(cd.filter(), state=None)
async def button_press(call: types.CallbackQuery, callback_data: dict):
    global action
    global num_id
    action = callback_data.get('action')
    num_id = callback_data.get('num_id')
    if not action == 'delete':
        await FSMEdit.value.set()
        await call.bot.send_message(
            call.message.chat.id, 
            'Введите новое значение',
            reply_markup=kba,
        )
    else:
        result = edit_number(action, num_id)
        if result:
            await bot.send_message(
                call.message.chat.id, 
                f'Номер удален',
                reply_markup=kbs,
            )
        else:
            await bot.send_message(
                call.message.chat.id, 
                'Команда использована неверно',
                reply_markup=kbs,
            )
    

@dp.message_handler(state=FSMEdit.value)
async def edit_value(message: types.Message, state: FSMContext):
    """
    Записывается значение и изменяется запись
    """
    async with state.proxy() as data:
        data['value'] = message.text
        result = edit_number(action, num_id, data['value'])
        if result:
            await bot.send_message(
                message.chat.id, 
                f'Данные изменены',
                reply_markup=kbs,
            )
        else:
            await bot.send_message(
                message.chat.id, 
                'Команда использована неверно',
                reply_markup=kbs,
            )
        
    await state.finish()
    

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
