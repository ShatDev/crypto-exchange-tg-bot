from random import randint
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from kb import inl_currencies_bep
from data_base import sql_add_bsc_data, sql_update_bsc_status
import requests
from bot_create import path
from handler import user
from config import bep_dict
from kb import inl_currencies_bep_rec, yn_bep, menu, sent_bsc, received_bsc


# состояния для машины состояний
class Form(StatesGroup):
    currency = State()
    currency_receive = State()
    wallet = State()
    amount_state = State()
    amount_receive_state = State()
    status_p = State()
    number_p = State()


# выбор токена (отдать)
async def bep_currencies_exc(callback: types.CallbackQuery):
    await Form.currency.set()
    await callback.message.edit_caption('Выберите токен, который вы отдаёте (<b>BSC</b>):', reply_markup=inl_currencies_bep)

# выбор токена(получить)
async def want_exch_bep(callback: types.CallbackQuery, state: FSMContext):
    global sending_token_bep
    sending_token_bep = callback.data.replace('_bep_e', '')
    if sending_token_bep == 'usdt':
        await callback.message.edit_caption(f'Вы отправляете USDT (<b>сеть BSC</b>)\n{"-" * 28}\nВыберите токен, который получите', reply_markup=inl_currencies_bep_rec)
    if sending_token_bep == 'busd':
        await callback.message.edit_caption(f'Вы отправляете BUSD (<b>сеть BSC</b>)\n{"-" * 28}\nВыберите токен, который получите', reply_markup=inl_currencies_bep_rec)
    if sending_token_bep == 'eth':
        await callback.message.edit_caption(f'Вы отправляете Ethereum (<b>сеть BSC</b>)\n{"-" * 28}\nВыберите токен, который получите (SOL недоступен)', reply_markup=inl_currencies_bep_rec)
    if sending_token_bep == 'ltc':
        await callback.message.edit_caption(f'Вы отправляете Litecoin (<b>сеть BSC</b>)\n{"-" * 33}\nВыберите токен, который получите', reply_markup=inl_currencies_bep_rec)
    if sending_token_bep == 'sol':
        await callback.message.edit_caption(f'Вы отправляете Solana (<b>сеть BSC</b>)\n{"- "*30}\nВыберите токен, который получите', reply_markup=inl_currencies_bep_rec)
    if sending_token_bep == 'xrp':
        await callback.message.edit_caption(f'Вы отправляете XRP (<b>сеть BSC</b>)\n{"- "*27}\nВыберите токен, который получите', reply_markup=inl_currencies_bep_rec)
    async with state.proxy() as data:
        data['currency'] = sending_token_bep.upper()
    await Form.next()


# запись в состояние актива и ввод адреса кошелька
async def bep_currencies_rec(callback: types.CallbackQuery, state: FSMContext):
    global tkn_rec_bep
    tkn_rec_bep = callback.data.replace('_bep_rec', '')
    if tkn_rec_bep != sending_token_bep:
        async with state.proxy() as data:
            data['currency_receive'] = tkn_rec_bep.upper()
        await Form.next()
        await callback.message.edit_caption('''
Введите адрес, куда отправить токены (<b>BEP20</b>)
Как правильно отправить адрес?\n
Правильный формат: <b>0x123F34c4562D756907db2fb5304B52BdcA356367</b>
''')
    else:
        await callback.message.edit_caption('К сожалению, нельзя обменять два одиннаковых токена. Выберите токены заново, пожалуйста.', reply_markup=menu)
        await state.finish()


# запись в состояние адреса кошелька и ввод кол-ва токенов
async def addresss_bep(message: types.Message, state: FSMContext):
    global addr, am_rec
    addr = message.text 
    async with state.proxy() as data:
        data['wallet'] = message.text
    await Form.next() 
    await message.answer_photo(user.photo1, f'''
Введите количество токенов, которое вы хотите обменять\n{"-" * 40}
<i>Текущий курс: 1 {sending_token_bep.upper()} = {(am_rec := requests.get(url=f'https://min-api.cryptocompare.com/data/price?fsym={sending_token_bep}&tsyms={tkn_rec_bep}{path}').json()[tkn_rec_bep.upper()])} {tkn_rec_bep.upper()}</i>'''
    )


# запись в состояние кол-ва токенов и вывод сообщения-подтверждения данных
async def amount_bep(message: types.Message, state: FSMContext):
    global amount_bep_var
    amount_bep_var = float(message.text)
    async with state.proxy() as data:
        data['amount_state'] = amount_bep_var
    await Form.next()
    async with state.proxy() as data:
        data['amount_receive_state'] = float(am_rec) * amount_bep_var
    await message.answer_photo(user.photo1, f'''
Адрес получения: <b>{addr}</b>\n{"-" * 16}
Отправляете: <b>{amount_bep_var} {sending_token_bep.upper()}</b>
Получаете: <b>{amount_bep_var * float(am_rec)} {tkn_rec_bep.upper()}</b>
Сеть: <b>BSC</b>
Проверьте правильность введённых данных.''', reply_markup=yn_bep
)
    await Form.next()


# создание заявки
async def info_bep(callback: types.CallbackQuery, state: FSMContext):
    global numb
    await callback.message.answer_photo(user.photo1, f'''
Заявка № <code>{(numb := str(randint(1, 100)) + str(callback.from_user.id))}</code> создана\n{"-" * 40}
Отправьте {amount_bep_var} {sending_token_bep.upper()} на адрес
<code>{bep_dict[sending_token_bep][0]}</code>''', reply_markup=sent_bsc
    )
    async with state.proxy() as data:
        data['status_p'] = 'создана'
    await Form.next()

    async with state.proxy() as data:
        data['number_p'] = numb
    await sql_add_bsc_data(state)
    await state.finish()


# изменение состояния заявки (отмена, оплачена)
async def sent_money_bep(callback: types.CallbackQuery):
    if callback.data == 'sent_bsc':
        await sql_update_bsc_status('оплачена', addr, numb)
        await callback.message.edit_caption('<b>Отлично. Платёж поступит в течение 10 минут 🕛</b>', reply_markup=received_bsc)
    else:
        await sql_update_bsc_status('отменена', addr, numb)
        await callback.message.edit_caption('<b>Платёж отменён</b>', reply_markup=menu) 


# изменение состояние заявки на выполнена с последующим выводом инл. кнопки перехода в меню
async def received_money_bep(callback: types.CallbackQuery):
    if callback.data == 'received_bsc':
        await sql_update_bsc_status('выполнена', addr, numb)
        await callback.message.edit_caption(f'''
Отлично! Заявка была выполнена успешно! 🎉
{"-" * 40}\n
<b>Спасибо за то, что пользуетесь нашим ботом! 💟</b>''', reply_markup=menu)


# хэндлеры
def register_addramount_bep(dp: Dispatcher):
    dp.register_callback_query_handler(bep_currencies_exc, text='bep20', state=None)
    dp.register_callback_query_handler(want_exch_bep, Text(endswith='_bep_e'), state=Form.currency)
    dp.register_callback_query_handler(bep_currencies_rec, Text(endswith='_bep_rec'), state=Form.currency_receive)
    dp.register_message_handler(addresss_bep, Text(startswith='0x'), state=Form.wallet)
    dp.register_message_handler(amount_bep, state=Form.amount_state)
    dp.register_callback_query_handler(info_bep, text='yes_bep', state=Form.status_p)
    dp.register_callback_query_handler(info_bep, text='menu')
    dp.register_callback_query_handler(sent_money_bep, text='sent_bsc')
    dp.register_callback_query_handler(sent_money_bep, text='cancel_bsc')
    dp.register_callback_query_handler(received_money_bep, text='received_bsc')