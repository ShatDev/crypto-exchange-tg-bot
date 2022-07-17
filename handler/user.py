from bot_create import dp
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from kb import inl_kb_exch, inl_kb_netw, menu
from networks import register_addramount_bep, register_addramount_trx

photo1 = 'https://ibb.co/JpLsZCX'
# photo2 = 'blob:https://web.telegram.org/05876bb5-f6a9-4e68-9463-50cb4da31c47'


# старт
async def start_cm(message: types.Message):
    await message.answer_photo(photo1, 'Здравствуйте, уважаемый пользователь.\nЯ - бот-<b>обменник</b>!\nК Вашим услугам 😏', reply_markup=inl_kb_exch)


# главное меню
async def menu_get(callback: types.CallbackQuery):
    await callback.message.edit_caption(f'<b>Главное меню.</b>\n{"-" * 15}', reply_markup=inl_kb_exch)


# Выбор сети
async def network_sel(callback: types.CallbackQuery):
    await callback.message.edit_caption('Выберите сеть:', reply_markup=inl_kb_netw)
# бск
    register_addramount_bep(dp)
# трон
    register_addramount_trx(dp)


# хэндлеры
def register_handler_user(dp: Dispatcher):
    dp.register_message_handler(start_cm, commands='start')
    dp.register_callback_query_handler(menu_get, text='menu')
    dp.register_callback_query_handler(network_sel, text='exchange')
