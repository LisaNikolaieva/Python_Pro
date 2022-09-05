import os

import psycopg2
from flask import Flask, request
import datetime
import sqlite3

import models
from models import db
from models import Currency, Account, Deposit, Rating, Transaction

from flask_migrate import Migrate

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db1.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:example@ps:5432/postgres'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STR')

db.init_app(app)
migrate=Migrate(app, db)


#psycopg2.connect(dbname="postgres", user="postgres", password="example", host='pythonproject2_db_1', port='5432')


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_data(query):
    conn = sqlite3.connect('db1.db')
    conn.row_factory = dict_factory
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
    # res = get_data(f"SELECT * FROM Currency")
    res = Currency.query.all()
    return [item.to_dict() for item in res]


@app.get("/currency/<currency_name>")
def show_currency_name(currency_name):
    # res = get_data(f"SELECT * FROM Currency WHERE name='{currency_name}'")
    res = Currency.query.filter_by(name=currency_name).all()
    return [item.to_dict() for item in res]


@app.get("/currency/<currency_name>/review")
def show_currency_review(currency_name):
    #res = get_data(f"SELECT currency_name, ROUND(AVG(rating),1) FROM Rating GROUP BY currency_name")
    currency_rating = dict(
        db.session.query(
            db.func.avg(models.Rating.rating).label('rate')
        ).filter(
            models.Rating.currency_name == currency_name
        ).first()
    )['rate']
    return {'avg': round(currency_rating,2)}


@app.get("/currency/trade/<currency_name_1>/<currency_name_2>")
def show_currency_trade(currency_name_1, currency_name_2):
    date_now = datetime.datetime.now().strftime('%d.%m.%Y')
    # res = get_data(f"""SELECT round(
    #                     (SELECT USD_relative_value FROM Currency WHERE name='{currency_name_1}' AND date='{date_now}')/
    #                     (SELECT USD_relative_value FROM Currency WHERE name='{currency_name_2}' AND date='{date_now}'),
    #                     1)""")

    res1 = Currency.query.filter_by(name=currency_name_1, date=date_now).first()
    res2 = Currency.query.filter_by(name=currency_name_2, date=date_now).first()
    return {'value': res1.USD_relative_value / res2.USD_relative_value}


@app.get("/user/<user_id>")
def show_balance(user_id):
    # res = get_data(f"SELECT currency_name, balance FROM Account WHERE user_id = '{user_id}'")
    res = Account.query.filter_by(user_id=user_id).first()
    return {'cur_name': res.currency_name, 'balance': res.balance}


@app.get("/user/<user_id>/history")
def show_user_history(user_id):
    # res = get_data(f"SELECT * FROM 'Transaction' WHERE user='{user_id_initial}'")
    res = Transaction.query.filter_by(user_id_initial=user_id).first()
    return {'id': res.id, 'user_id_initial': res.user_id_initial, 'operation_type': res.operation_type,
            'currency_num_spent': res.currency_num_spent, 'currency_num_obtained': res.currency_num_obtained,
            'currency_name_spent': res.currency_name_spent, 'currency_name_obtained': res.currency_name_obtained,
            'date_time': res.date_time, 'user_id_final': res.user_id_final, 'commission': res.commission}


@app.get("/user/<user_id>/deposit")
def show_user_deposit(user_id):
    # res = get_data(f"SELECT * FROM Deposit WHERE user_id='{user_id}'")
    res = Deposit.query.filter_by(user_id=user_id).first()
    return {'id': res.id, 'user_id': res.user_id, 'opening_date': res.opening_date, 'closing_date': res.closing_date,
            'balance': res.balance, 'interest_rate': res.interest_rate, 'dividends_account': res.dividends_account,
            'dividends_date': res.dividends_date}


#### POST ####

@app.post("/currency/<currency_name>/review")
def add_currency_rating(currency_name):
    request_data = request.get_json()
    rating = request_data['rating']
    comment = request_data['comment']
    rating_obj = Rating(currency_name=currency_name, rating=rating, comment=comment)
    db.session.add(rating_obj)
    db.session.commit()
    # get_data(f"INSERT INTO Rating (currency_name, rating, comment) VALUES ('{currency_name}', {rating}, '{comment}' )")
    return 'ok'


@app.post("/currency/trade/<currency_name_1>/<currency_name_2>")
def exchange(currency_name_1, currency_name_2):
    date_now = datetime.datetime.now().strftime('%d.%m.%Y')
    user_id = 1
    amount1 = request.get_json()['amount']
    commission = 0.2 * amount1
    amount1c = amount1 + commission

    user_balance1 = Account.query.filter_by(user_id=user_id, currency_name=currency_name_1).first().balance
    user_balance2 = Account.query.filter_by(user_id=user_id, currency_name=currency_name_2).first().balance

    cur1_USD_relative_value = Currency.query.filter_by(name=currency_name_1, date=date_now).first().USD_relative_value
    cur2_USD_relative_value = Currency.query.filter_by(name=currency_name_2, date=date_now).first().USD_relative_value

    need_cur2 = amount1 * cur1_USD_relative_value / cur2_USD_relative_value

    existing_amount_currency1 = Currency.query.filter_by(name=currency_name_1, date=date_now).first().available_quantity
    existing_amount_currency2 = Currency.query.filter_by(name=currency_name_2, date=date_now).first().available_quantity

    if (user_balance1 >= amount1) and (existing_amount_currency2 > need_cur2):

        # get_data(f"UPDATE Currency SET available_quantity={existing_amount_currency2 - need_cur2} WHERE name='{currency_name_2}' AND date='{date_now}'")
        # get_data(f"UPDATE Currency SET available_quantity={existing_amount_currency1 + amount1c} WHERE name='{currency_name_1}' AND date='{date_now}'")

        # get_data( f"UPDATE Account SET balance={user_balance1 - amount1c} WHERE user_id='{user_id}' AND currency_name='{currency_name_1}'")
        # get_data(f"UPDATE Account SET balance={user_balance2 + need_cur2} WHERE user_id='{user_id}' AND currency_name='{currency_name_2}'")

        Currency.query.filter_by(name=currency_name_2, date=date_now).update(dict(available_quantity=(existing_amount_currency2 - need_cur2)))
        Currency.query.filter_by(name=currency_name_1, date=date_now).update(dict(available_quantity=(existing_amount_currency1 + amount1c)))

        Account.query.filter_by(user_id=user_id, currency_name=currency_name_1).update(dict(balance=(user_balance1 - amount1c)))
        Account.query.filter_by(user_id=user_id, currency_name=currency_name_2).update(dict(balance=(user_balance2 + need_cur2)))

        transaction_obj = Transaction(user_id_initial=user_id, operation_type='exchange', currency_num_spent=amount1,
                                      currency_num_obtained=need_cur2, currency_name_spent=currency_name_1,
                                      currency_name_obtained=currency_name_2, date_time=date_now, user_id_final=user_id,
                                      commission=commission)
        db.session.add(transaction_obj)
        db.session.commit()

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

if __name__ == '__main__':
    app.run(host='0.0.0.0')
