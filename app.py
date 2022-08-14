from flask import Flask
import sqlite3

app = Flask(__name__)


def get_data(query):
    conn = sqlite3.connect('db1.db')
    cursor = conn.execute(query)
    res = cursor.fetchall()
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
    res = get_data(f"""SELECT
                    round((SELECT USD_relative_value FROM Currency WHERE date='14.08.2022' AND name='{currency_name_1}')/
                    (SELECT USD_relative_value FROM Currency WHERE date='14.08.2022' AND name='{currency_name_2}'),1)""")
    return res


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





"""
@app.route("/currency/<currency_name>/review", methods=['POST', 'PUT', 'DELETE'])
def show_currency_review(currency_name):
    return f'Review: {currency_name}'


@app.route("/currency/trade/<currency_name_1>/<currency_name_2>", methods=['POST'])
def show_currency_trade(currency_name_1, currency_name_2):
    return f'Trade: {currency_name_1} {currency_name_2}'


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
