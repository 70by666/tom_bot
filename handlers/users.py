from aiogram import Dispatcher, types

from keyboards.other import kb_start
from keyboards.users import kb_start_inline, get_kb_start_inline
from services.api import get_user_from_id, get_url_for_auth
from settings import bot, cd_start_2


async def auth(message: types.Message):
    global msg_no_auth
    
    result = get_user_from_id(message.from_user.id)
    if result:
        await bot.send_message(
            message.chat.id, 
            f'Вы авторизованы как {result["username"]}'
            ''
            '\n\n\n',
            reply_markup=kb_start,
        )  
    else: 
        msg_no_auth = await bot.send_message(
            message.chat.id, 
            'Вы не авторизованы, чтобы получить ссылку для авторизации, '
            'нажмите на ссылку'
            '\n\n\n',
            reply_markup=kb_start_inline,
        )


# async def auth(message: types.Message):
#     result = get_user_from_id(message.from_user.id)
#     if result:
#         await bot.send_message(
#             message.chat.id, 
#             f'Вы авторизованы как {result["username"]}'
#             ''
#             '\n\n\n',
#             reply_markup=kb_start,
#         )  
#     else: 
#         msg_no_auth = await bot.send_message(
#             message.chat.id, 
#             'Вы не авторизованы, чтобы получить ссылку для авторизации, '
#             'нажмите на ссылку'
#             '\n\n\n',
#             # reply_markup=kb_start_inline,
#         )
#         await bot.send_message(
#             message.chat.id, 
#             '1',
#             reply_markup=get_kb_start_inline(msg_no_auth.message_id),
#         )
        

async def get_url(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    try:
        await callback.bot.edit_message_text(
            chat_id=user_id,
            message_id=msg_no_auth.message_id,
            # message_id=callback_data.get('num_id'),
            text=f'Чтобы привязать Телеграм к аккаунту на сайте, '
            'нужно быть авторизованным на сайте\n'
            f'{get_url_for_auth(user_id)}',
            reply_markup=kb_start,
        )
    except NameError:
        await callback.bot.send_message(
            user_id,
            f'Чтобы привязать Телеграм к аккаунту на сайте, '
            'нужно быть авторизованным на сайте\n'
            f'{get_url_for_auth(user_id)}',
            reply_markup=kb_start,
        )


async def profile(message: types.Message):
    result = get_user_from_id(message.from_user.id)
    if result:
        await bot.send_message(
            message.chat.id, 
            f'Ник: {result["username"]}\n'
            f'Почта: {result["email"]}\n'
            f'Имя: {result["first_name"]}\n'
            f'Фамилия: {result["last_name"]}\n'
            f'Родился(ась): {result["birth_day"]}\n'
            f'Дата регистрации: {result["date_joined"]}\n'
            f'О себе: {result["bio"]}\n'
            '\n\n\n',
            reply_markup=kb_start,
        )  
    else: 
        await bot.send_message(
            message.chat.id, 
            'Вы не авторизованы, чтобы получить ссылку для авторизации, '
            'нажмите на ссылку'
            '\n\n\n',
            reply_markup=kb_start_inline,
        )


def register_handlers_users(dp: Dispatcher):
    dp.register_message_handler(auth, commands=['auth'])
    # dp.register_callback_query_handler(get_url, cd_start_2.filter())
    dp.register_callback_query_handler(get_url, text='get_url')
    dp.register_message_handler(profile, commands=['profile'])
