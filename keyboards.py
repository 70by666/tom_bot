from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

ks1 = KeyboardButton('/start')
ks2 = KeyboardButton('/number')
ks3 = KeyboardButton('/addnumber')
ks4 = KeyboardButton('/убратькнопки')

kbs = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
kbs.add(ks1, ks2, ks3, ks4)


kn1 = KeyboardButton('last_name')
kn2 = KeyboardButton('first_name')
kn3 = KeyboardButton('patronymic')
kn4 = KeyboardButton('/stop')

kbn = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
kbn.add(kn1, kn2, kn3, kn4)


ka1 = KeyboardButton('/stop')
kba = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
kba.add(ka1)
