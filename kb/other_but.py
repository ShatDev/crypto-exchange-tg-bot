from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# other
men_but = InlineKeyboardButton(text='Меню', callback_data='menu')
menu = InlineKeyboardMarkup(row_width=1).add(men_but)


# кнопка для подтверждения введенных польз. данных (бск)
yn_bep = InlineKeyboardMarkup(row_width=2)
yes_bep = InlineKeyboardButton(text='Далее', callback_data='yes_bep')
yn_bep.add(yes_bep)


# кнопка для подтверждения введенных польз. данных (трон)
yn_trx = InlineKeyboardMarkup(row_width=2)
yes_tr = InlineKeyboardButton(text='Далее', callback_data='yes_trx')
yn_trx.add(yes_tr)


# кнопки для подтверждения оплаты (бск)
sent_bsc = InlineKeyboardMarkup(row_width=2)
s_b_bsc = InlineKeyboardButton('Оплатил', callback_data='sent_bsc')
cancel_bsc = InlineKeyboardButton('Отмена', callback_data='cancel_bsc')
sent_bsc.add(s_b_bsc, cancel_bsc)
# кнопка для подтверждения выполнения заявки (бск)
received_bsc = InlineKeyboardMarkup(row_width=1)
rc_bsc_but = InlineKeyboardButton('Я получил платёж', callback_data='received_bsc')
received_bsc.add(rc_bsc_but)


# кнопки для подтверждения оплаты (трон)
sent_tron = InlineKeyboardMarkup(row_width=2)
s_b_tron = InlineKeyboardButton('Оплатил', callback_data='sent_tron')
cancel_trx = InlineKeyboardButton('Отмена', callback_data='cancel_trx')
sent_tron.add(s_b_tron, cancel_bsc)
# кнопка для подтверждения выполнения заявки (трон)
received_trx = InlineKeyboardMarkup(row_width=1)
rc_trx_but = InlineKeyboardButton('Я получил платёж', callback_data='received_trx')
received_trx.add(rc_trx_but)
