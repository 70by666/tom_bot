from aiogram import executor

from handlers import other, users
from settings import dp

users.register_handlers_users(dp)
other.register_handlers_other(dp)
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
