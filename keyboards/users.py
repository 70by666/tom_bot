from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

kb_start_inline = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton('Получить ссылку', callback_data='get_url')
)
