from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "<p>Hello, Lisa!</p>"


@app.route("/currency", methods=['GET'])
def show_currency():
    return f'Currency'


@app.route("/currency/<currency_name>", methods=['GET'])
def show_currency_name(currency_name):
    return f'Currency: {currency_name}'


@app.route("/currency/<currency_name>/review", methods=['GET', 'POST', 'PUT', 'DELETE'])
def show_currency_review(currency_name):
    return f'Review: {currency_name}'


@app.route("/currency/trade/<currency_name_1>/<currency_name_2>", methods=['GET', 'POST'])
def show_currency_trade(currency_name_1, currency_name_2):
    return f'Trade: {currency_name_1} {currency_name_2}'


@app.route("/user", methods=['GET'])
def show_user():
    return f'User'


@app.route("/user/transfer", methods=['POST'])
def show_user_transfer():
    return f'User Transfer'


@app.route("/user/history", methods=['GET'])
def show_user_history():
    return f'User History'


@app.route("/user/deposit", methods=['GET', 'POST'])
def show_user_deposit():
    return f'User Deposit'


@app.route("/user/deposit/<deposit_id>", methods=['GET', 'POST'])
def show_user_deposit_id(deposit_id):
    return f'User Deposit id: {deposit_id}'


@app.route("/deposit/<currency_name>", methods=['GET'])
def show_deposit_currency(currency_name):
    return f'Deposit: {currency_name}'