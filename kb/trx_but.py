from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# trx20 currencies to exchange (активы, которые отдаёте)
inl_currencies_trx = InlineKeyboardMarkup(row_width=2)
usdt_trx_but = InlineKeyboardButton(text='USDT', callback_data='usdt_trx_e')
eth_trx_but = InlineKeyboardButton(text='ETH', callback_data='eth_trx_e')
ltc_trx_but = InlineKeyboardButton(text='LTC', callback_data='ltc_trx_e')
xrp_trx_but = InlineKeyboardButton(text='XRP', callback_data='xrp_trx_e')
inl_currencies_trx.add(eth_trx_but, ltc_trx_but, xrp_trx_but, usdt_trx_but)


# trx20 currencies to receive (активы, которые получаете)
inl_currencies_trx_rec = InlineKeyboardMarkup(row_width=2)
usdt_trx_butr = InlineKeyboardButton(text='USDT', callback_data='usdt_trx_rec')
eth_trx_butr = InlineKeyboardButton(text='ETH', callback_data='eth_trx_rec')
ltc_trx_butr = InlineKeyboardButton(text='LTC', callback_data='ltc_trx_rec')
xrp_trx_butr = InlineKeyboardButton(text='XRP', callback_data='xrp_trx_rec')
inl_currencies_trx_rec.add(eth_trx_butr, ltc_trx_butr, xrp_trx_butr, usdt_trx_butr)
