from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# bep20 currencies to exchange (активы, которые отдаёте)
inl_currencies_bep = InlineKeyboardMarkup(row_width=2)
usdt_bep_but = InlineKeyboardButton(text='USDT', callback_data='usdt_bep_e')
busd_bep_but = InlineKeyboardButton(text='BUSD', callback_data='busd_bep_e')
eth_bep_but = InlineKeyboardButton(text='ETH', callback_data='eth_bep_e')
ltc_bep_but = InlineKeyboardButton(text='LTC', callback_data='ltc_bep_e')
sol_bep_but = InlineKeyboardButton(text='SOL', callback_data='sol_bep_e')
xrp_bep_but = InlineKeyboardButton(text='XRP', callback_data='xrp_bep_e')
inl_currencies_bep.add(eth_bep_but, ltc_bep_but, sol_bep_but, xrp_bep_but, usdt_bep_but, busd_bep_but)


# bep20 currencies to receive (активы, которые получаете)
inl_currencies_bep_rec = InlineKeyboardMarkup(row_width=2)
usdt_bep_butr = InlineKeyboardButton(text='USDT', callback_data='usdt_bep_rec')
busd_bep_butr = InlineKeyboardButton(text='BUSD', callback_data='busd_bep_rec')
eth_bep_butr = InlineKeyboardButton(text='ETH', callback_data='eth_bep_rec')
ltc_bep_butr = InlineKeyboardButton(text='LTC', callback_data='ltc_bep_rec')
sol_bep_butr = InlineKeyboardButton(text='SOL', callback_data='sol_bep_rec')
xrp_bep_butr = InlineKeyboardButton(text='XRP', callback_data='xrp_bep_rec')
inl_currencies_bep_rec.add(eth_bep_butr, ltc_bep_butr, sol_bep_butr, xrp_bep_butr, usdt_bep_butr, busd_bep_butr)
