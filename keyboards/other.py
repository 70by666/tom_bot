from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

kr = types.ReplyKeyboardRemove()

kb_start = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
kb_start.add(
    KeyboardButton('/start'), KeyboardButton('/auth'), 
    KeyboardButton('/removekb')
)
