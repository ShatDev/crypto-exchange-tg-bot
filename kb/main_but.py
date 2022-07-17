from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# кнопка для перехода к выбору сети
inl_kb_exch = InlineKeyboardMarkup(row_width=1)
exch_but = InlineKeyboardButton(text='Обмен', callback_data='exchange')
inl_kb_exch.add(exch_but)


# кнопки сетей
inl_kb_netw = InlineKeyboardMarkup(row_width=2)
bep_but = InlineKeyboardButton(text='BEP20', callback_data='bep20')
trx_but = InlineKeyboardButton(text='TRON', callback_data='trx20')
inl_kb_netw.add(bep_but, trx_but)