from aiogram import Dispatcher, types

from keyboards.other import kb_start
from keyboards.users import kb_start_inline
from services.api import get_user_from_id, get_url_for_auth
from settings import bot


async def auth(message: types.Message):
    global msg_no_auth
    
    result = get_user_from_id(message.from_user.id)
    if result:
        await bot.send_message(
            message.chat.id, 
            f'Вы авторизованы как {result["username"]}'
            ''
            '\n\n\n'
            '/chatgpt [text]\n',
            reply_markup=kb_start,
        )  
    else: 
        msg_no_auth = await bot.send_message(
            message.chat.id, 
            'Вы не авторизованы, чтобы получить ссылку для авторизации, '
            'нажмите на ссылку'
            '\n\n\n'
            '/chatgpt [text]\n',
            reply_markup=kb_start_inline,
        )  


async def get_url(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await callback.bot.edit_message_text(
        chat_id=user_id,
        message_id=msg_no_auth.message_id,
        text=get_url_for_auth(user_id),
    )


def register_handlers_users(dp: Dispatcher):
    dp.register_message_handler(auth, commands=['auth'])
    dp.register_callback_query_handler(get_url, text='get_url')
