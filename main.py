from aiogram.utils import executor
from bot_create import dp
from handler import user
from data_base import sql3_connect


# запуск бота и бд
def on_startup():
    print('Bot starting proccess...')
    sql3_connect()


 # вызов функции, в которую записаны хэндлеры
user.register_handler_user(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup())
