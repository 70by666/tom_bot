from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

k1 = KeyboardButton('/start')
k2 = KeyboardButton('/number')
k3 = KeyboardButton('/убратькнопки')

kb = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
kb.add(k1, k2, k3)
