from flask import Flask, request
import datetime
import sqlite3

app = Flask(__name__)

date_now = datetime.datetime.now().strftime('%d.%m.%Y')


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_data(query):
    conn = sqlite3.connect('db1.db')
    # conn.row_factory = dict_factory
    cursor = conn.execute(query)
    res = cursor.fetchall()
    conn.commit()
    conn.close()
    return res


@app.route("/")
def hello():
    return "<p>Hello, Lisa!</p>"


#### GET ####

@app.get("/currency")
def currency_list():
    res = get_data(f"SELECT * FROM Currency")
    return res


@app.get("/currency/<currency_name>")
def show_currency_name(currency_name):
    res = get_data(f"SELECT * FROM Currency WHERE name='{currency_name}'")
    return res


@app.get("/currency/review")
def show_currency_review():
    res = get_data(f"SELECT currency_name, ROUND(AVG(rating),1) FROM Rating GROUP BY currency_name")
    return res


@app.get("/currency/trade/<currency_name_1>/<currency_name_2>")
def show_currency_trade(currency_name_1, currency_name_2):
    res0 = get_data(f"""SELECT round(
                        (SELECT USD_relative_value FROM Currency WHERE date='14.08.2022' AND name='{currency_name_1}')/
                        (SELECT USD_relative_value FROM Currency WHERE date='14.08.2022' AND name='{currency_name_2}'),
                        1)""")
    res1 = get_data(f"""SELECT round(
                        (SELECT USD_relative_value FROM Currency WHERE name='{currency_name_1}' ORDER BY date DESC LIMIT 1)/
                        (SELECT USD_relative_value FROM Currency WHERE name='{currency_name_2}' ORDER BY date DESC LIMIT 1),
                        1)""")
    res2 = get_data(f"""SELECT round(
                        (SELECT USD_relative_value FROM Currency WHERE name='{currency_name_1}' AND date='{date_now}')/ 
                        (SELECT USD_relative_value FROM Currency WHERE name='{currency_name_2}' AND date='{date_now}'),
                        1)""")
    return res2


@app.get("/user/<user_id>")
def show_balance(user_id):
    res = get_data(f"SELECT currency_name, balance FROM Account WHERE user_id = '{user_id}'")
    return res


@app.get("/user/<user_id>/history")
def show_user_history(user_id):
    res = get_data(f"SELECT * FROM 'Transaction' WHERE user='{user_id}'")
    return res


@app.get("/user/<user_id>/deposit")
def show_user_deposit(user_id):
    res = get_data(f"SELECT * FROM Deposit WHERE user_id='{user_id}'")
    return res


#### POST ####

@app.post("/currency/<currency_name>/review")
def add_currency_rating(currency_name):
    request_data = request.get_json()
    rating = request_data['rating']
    comment = request_data['comment']
    get_data(f"INSERT INTO Rating (currency_name, rating, comment) VALUES ('{currency_name}', {rating}, '{comment}' )")
    return 'ok'


@app.post("/currency/trade/<currency_name_1>/<currency_name_2>")
def exchange(currency_name_1, currency_name_2):
    user_id = 1
    amount1 = request.get_json()['amount']
    comission = 0.2 * amount1
    amount1c = amount1 + comission

    user_balance1 = \
        get_data(f"""SELECT balance FROM Account WHERE user_id={user_id} AND currency_name='{currency_name_1}'""")[0][0]
    user_balance2 = \
        get_data(f"""SELECT balance FROM Account WHERE user_id={user_id} AND currency_name='{currency_name_2}'""")[0][0]

    cur1_USD_relative_value = \
        get_data(f"SELECT USD_relative_value FROM Currency WHERE name='{currency_name_1}' AND date='{date_now}'")[0][0]
    cur2_USD_relative_value = \
        get_data(f"SELECT USD_relative_value FROM Currency WHERE name='{currency_name_2}' AND date='{date_now}'")[0][0]

    print(f"aaaaaaaaaaaaaaaaaa{user_balance1}")
    need_cur2 = amount1 * cur1_USD_relative_value / cur2_USD_relative_value
    print(f"bbbbbb{need_cur2}")
    existing_amount_currency1 = \
        get_data(f"SELECT available_quantity FROM Currency WHERE name='{currency_name_1}' AND date='{date_now}'")[0][0]
    existing_amount_currency2 = \
        get_data(f"SELECT available_quantity FROM Currency WHERE name='{currency_name_2}' AND date='{date_now}'")[0][0]

    if (user_balance1 >= amount1) and (existing_amount_currency2 > need_cur2):
        get_data(
            f"UPDATE Currency SET available_quantity={existing_amount_currency2 - need_cur2} WHERE name='{currency_name_2}' AND date='{date_now}'")
        get_data(
            f"UPDATE Currency SET available_quantity={existing_amount_currency1 + amount1c} WHERE name='{currency_name_1}' AND date='{date_now}'")

        get_data(
            f"UPDATE Account SET balance={user_balance1 - amount1c} WHERE user_id='{user_id}' AND currency_name='{currency_name_1}'")
        get_data(
            f"UPDATE Account SET balance={user_balance2 + need_cur2} WHERE user_id='{user_id}' AND currency_name='{currency_name_2}'")

        get_data(
            f"""INSERT INTO "Transaction" (user_id_initial, operation_type, currency_num_spent, currency_num_obtained, currency_name_spent, currency_name_obtained, date_time, user_id_final, commission) VALUES ({user_id}, 'exchange', {amount1}, {need_cur2}, '{currency_name_1}', '{currency_name_2}', '{date_now}', {user_id}, {comission})""")
        return 'ok'
    else:
        return 'not ok'


"""
# @app.route("/currency/<currency_name>/review", methods=['PUT', 'DELETE'])
# def show_currency_review(currency_name):
#     return f'Review: {currency_name}'
# 




@app.route("/user/transfer", methods=['POST'])
def show_user_transfer():
    return f'User Transfer'



@app.route("/user/deposit", methods=['POST'])
def show_user_deposit():
    return f'User Deposit'


@app.route("/user/deposit/<deposit_id>", methods=['POST'])
def show_user_deposit_id(deposit_id):
    return f'User Deposit id: {deposit_id}'
"""
