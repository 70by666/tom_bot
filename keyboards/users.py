from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from settings import cd_start_2

kb_start_inline = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton('Получить ссылку', callback_data='get_url')
)


def get_kb_start_inline(msg_id):
    kb_start_inline = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton('Получить ссылку 2', callback_data=cd_start_2.new(
            num_id=msg_id,
        )),
    )

    return kb_start_inline
