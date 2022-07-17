import sqlite3


# подключиться к бд
def sql3_connect():
    global base, cur
    base = sqlite3.connect('database.db')
    cur = base.cursor()
    if base:
        print('CONNECTED TO DATABASE')
    base.execute('''
    CREATE TABLE IF NOT EXISTS bsc(currency TEXT, currency_receive TEXT, 
    wallet TEXT, amount TEXT, amount_receive TEXT, status TEXT, id TEXT)
    ''')
    base.execute('''
    CREATE TABLE IF NOT EXISTS tron(currency TEXT, currency_receive TEXT, 
    wallet TEXT, amount TEXT, amount_receive TEXT, status TEXT, id TEXT)
    ''')
    base.commit()


# вставить данные пользователя бск (актив, получаемый актив, адрес кошелька, кол-во, получаемое кол-во, статус платежа, № заявки)
async def sql_add_bsc_data(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO bsc VALUES (?, ?, ?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()

# обновить статус платежа (бск)
async def sql_update_bsc_status(status, wallet, id_p):
    cur.execute('UPDATE bsc SET status = ? WHERE (status = "создана" OR status = "оплачена") AND wallet = ? AND id = ?', (status, wallet, id_p))
    base.commit()


# то же, что и строка 22, но для трона
async def sql_add_tron_data(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO tron VALUES (?, ?, ?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()

# то же, что и строка 28, но для трона
async def sql_update_tron_status(status, wallet, id_p):
    cur.execute('UPDATE tron SET status = ? WHERE (status = "создана" OR status = "оплачена") AND wallet = ? AND id = ?', (status, wallet, id_p))
    base.commit()