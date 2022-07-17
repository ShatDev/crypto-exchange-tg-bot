from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from handler import user
from bot_create import path
from data_base import sql_add_tron_data, sql_update_tron_status
from config import tron_dict
from kb import inl_currencies_trx, inl_currencies_trx_rec, yn_trx, menu, sent_tron, received_trx
from random import randint
import requests


# состояния для машины состояний
class Form_trx(StatesGroup):
    currency_tr = State()
    currency_receive_tr = State()
    wallet_tr = State()
    amount_state_tr = State()
    amount_receive_state_tr = State()
    status_p_tr = State()
    number_p_tr = State()


# выбор токена (отдать)
async def trx_currencies_exc(callback: types.CallbackQuery):
    await Form_trx.currency_tr.set()
    await callback.message.edit_caption('Выберите токен, который вы отдаёте (<b>TRON</b>):', reply_markup=inl_currencies_trx)


# выбор токена(получить)
async def want_exch_trx(callback: types.CallbackQuery, state: FSMContext):
    global sending_token_tr
    sending_token_tr = callback.data.replace('_trx_e', '')
    if sending_token_tr == 'usdt':
        await callback.message.edit_caption(f'Вы отправляете USDT! (<b>сеть TRON</b>)\n{"- "*29}\nВыберите токен, который получите', reply_markup=inl_currencies_trx_rec)
    if sending_token_tr == 'eth':
        await callback.message.edit_caption(f'Вы отправляете Ethereum! (<b>сеть TRON</b>)\n{"- "*29}\nВыберите токен, который получите', reply_markup=inl_currencies_trx_rec)
    if sending_token_tr == 'ltc':
        await callback.message.edit_caption(f'Вы отправляете Litecoin! (<b>сеть TRON</b>)\n{"- "*34}\nВыберите токен, который получите', reply_markup=inl_currencies_trx_rec)
    if sending_token_tr == 'xrp':
        await callback.message.edit_caption(f'Вы отправляете XRP! (<b>сеть TRON</b>)\n{"- "*28}\nВыберите токен, который получите', reply_markup=inl_currencies_trx_rec)
    async with state.proxy() as data:
        data['currency_tr'] = sending_token_tr.upper()
    await Form_trx.next()


# запись в состояние актива и ввод адреса кошелька
async def trx_currencies_rec(callback: types.CallbackQuery, state: FSMContext):
    global tkn_rec_trx
    tkn_rec_trx = callback.data.replace('_trx_rec', '')
    if tkn_rec_trx != sending_token_tr:
        async with state.proxy() as data:
            data['currency_receive_tr'] = tkn_rec_trx.upper()
        await Form_trx.next()
        await callback.message.edit_caption('''
Введите адрес, куда отправить токены (<b>TRON</b>)
Как правильно отправить адрес?\n
Правильный формат: <b>TMbyz1ZykG4XTXsfTMueKz79nhABocHuGs</b>
''')
        print(sending_token_tr, tkn_rec_trx)
    else:
        await callback.message.edit_caption('Нельзя обменивать два одиннаковых токена!', reply_markup=menu)
        await state.finish()


# запись в состояние адреса кошелька и ввод кол-ва токенов
async def addresss_trx(message: types.Message, state: FSMContext):
    global addr_trx, am_rec_tr
    addr_trx = message.text
    async with state.proxy() as data:
        data['wallet_tr'] = addr_trx
    await Form_trx.next()
    await message.answer_photo(user.photo1, f'''
Введите количество токенов, которое вы хотите обменять\n{"-" * 40}
<i>Текущий курс: 1 {sending_token_tr.upper()} = {(am_rec_tr := requests.get(url=f'https://min-api.cryptocompare.com/data/price?fsym={sending_token_tr}&tsyms={tkn_rec_trx}{path}').json()[tkn_rec_trx.upper()])} {tkn_rec_trx.upper()}</i>
'''
    )


# запись в состояние кол-ва токенов и вывод сообщения-подтверждения данных
async def amount_trx(message: types.Message, state: FSMContext):
    global amount_trx_var
    amount_trx_var = float(message.text)
    async with state.proxy() as data:
        data['amount_state_tr'] = amount_trx_var
    await Form_trx.next()
    async with state.proxy() as data:
        data['amount_receive_state_tr'] = amount_trx_var * float(am_rec_tr)
    await message.answer_photo(user.photo1, f'''
Адрес получения: <b>{addr_trx}</b>\n{"-"*16}
Отправляете: <b>{amount_trx_var} {sending_token_tr.upper()}</b>
Получаете: <b>{amount_trx_var * float(am_rec_tr)} {tkn_rec_trx.upper()}</b>
Сеть: <b>TRON</b>
Проверьте правильность введённых данных.''', reply_markup=yn_trx
)
    await Form_trx.next()


# создание заявки
async def info_trx(callback: types.CallbackQuery, state: FSMContext):
    global numb_tr
    await callback.message.answer_photo(user.photo1, f'''
Заявка  № <code>{(numb_tr := str(randint(1, 100)) + str(callback.from_user.id))}</code> создана.\n{"-" * 40}
Отправьте {amount_trx_var} {sending_token_tr.upper()} на адрес
<code>{tron_dict[sending_token_tr][0]}</code>''', reply_markup=sent_tron
    )
    async with state.proxy() as data:
        data['status_p_tr'] = 'создана'
    await Form_trx.next()
    
    async with state.proxy() as data:
        data['number_p_tr'] = numb_tr
    await sql_add_tron_data(state)
    await state.finish()


# изменение состояния заявки (отмена, оплачена)
async def sent_money_trx(callback: types.CallbackQuery):
    if callback.data == 'sent_tron':
        await sql_update_tron_status('оплачена', addr_trx, numb_tr)
        await callback.message.edit_caption('<b>Отлично. Платёж поступит в течение 10 минут 🕛</b>', reply_markup=received_trx)  
    else:
        await sql_update_tron_status('отменена', addr_trx, numb_tr)
        await callback.message.edit_caption('<b>Платёж отменён</b>', reply_markup=menu)


# изменение состояние заявки на выполнена с последующим выводом инл. кнопки перехода в меню
async def received_money_tron(callback: types.CallbackQuery):
    if callback.data == 'received_trx':
        await sql_update_tron_status('выполнена', addr_trx, numb_tr)
        await callback.message.edit_caption(f'''
Отлично! Заявка была выполнена успешно! 🎉
{"-" * 40}\n
<b>Спасибо за то, что пользуетесь нашим ботом! 💟</b>''', reply_markup=menu)


# хэндлеры
def register_addramount_trx(dp: Dispatcher):
    dp.register_callback_query_handler(trx_currencies_exc, text='trx20', state=None)
    dp.register_callback_query_handler(want_exch_trx, Text(endswith='_trx_e'), state=Form_trx.currency_tr)
    dp.register_callback_query_handler(trx_currencies_rec, Text(endswith='_trx_rec'), state=Form_trx.currency_receive_tr)
    dp.register_message_handler(addresss_trx, Text(startswith='T'), state=Form_trx.wallet_tr)
    dp.register_message_handler(amount_trx, state=Form_trx.amount_state_tr)
    dp.register_callback_query_handler(info_trx, text='yes_trx', state=Form_trx.status_p_tr)
    dp.register_callback_query_handler(info_trx, text='menu')
    dp.register_callback_query_handler(sent_money_trx, text='sent_tron')
    dp.register_callback_query_handler(sent_money_trx, text='cancel_trx')
    dp.register_callback_query_handler(received_money_tron, text='received_trx')
