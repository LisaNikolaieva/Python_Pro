import uuid

import psycopg2
from flask import Flask, request, session
import datetime
import sqlite3
import sqlalchemy

import celery_worker
import models

from models import Currency, Account, Deposit, Rating, Transaction
import database

from celery_worker import task1

app = Flask(__name__)
app.secret_key = 'djqevbwv'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db1.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:example@ps:5432/postgres'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STR')

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
    database.init_db()
    # res = get_data(f"SELECT * FROM Currency")
    res = Currency.query.all()
    return [item.to_dict() for item in res]


@app.get("/currency/<currency_name>")
def show_currency_name(currency_name):
    database.init_db()
    # res = get_data(f"SELECT * FROM Currency WHERE name='{currency_name}'")
    res = Currency.query.filter_by(name=currency_name).all()
    return [item.to_dict() for item in res]


@app.get("/currency/<currency_name>/review")
def show_currency_review(currency_name):
    database.init_db()
    currency_rating = dict(
        database.db_session.query(
            sqlalchemy.func.avg(models.Rating.rating).label('rate')
        ).filter(
            models.Rating.currency_name == currency_name
        ).first()
    )['rate']
    return {'avg': round(currency_rating, 2)}


# @app.get("/currency/trade/<currency_name_1>/<currency_name_2>")
# def show_currency_trade(currency_name_1, currency_name_2):
#     database.init_db()
#     date_now = datetime.datetime.now().strftime('%d.%m.%Y')
#     # res = get_data(f"""SELECT round(
#     #                     (SELECT USD_relative_value FROM Currency WHERE name='{currency_name_1}' AND date='{date_now}')/
#     #                     (SELECT USD_relative_value FROM Currency WHERE name='{currency_name_2}' AND date='{date_now}'),
#     #                     1)""")
#
#     res1 = Currency.query.filter_by(name=currency_name_1, date=date_now).first()
#     res2 = Currency.query.filter_by(name=currency_name_2, date=date_now).first()
#     return {'value': res1.USD_relative_value / res2.USD_relative_value}


@app.route("/user", methods = ['GET', 'POST'])
def show_balance():
    database.init_db()
    if request.method == 'GET':
        user_name = session.get('user_name')
        if user_name is None:
            return '''
            <html>
            <form method="post">
              <div class="container">
                <label for="uname"><b>Username</b></label>
                <input type="text" placeholder="Enter Username" name="uname" required>
            
                <label for="psw"><b>Password</b></label>
                <input type="password" placeholder="Enter Password" name="psw" required>
            
                <button type="submit">Login</button>
              </div>
            </form>
            </html>  
            '''
        else:
            # res = get_data(f"SELECT currency_name, balance FROM Account WHERE user_id = '{user_id}'")
            res = Account.query.filter_by(login=user_name).first()
            return {'cur_name': res.currency_name, 'balance': res.balance}

    if request.method == 'POST':
        user_login = request.form.get('uname')
        user_password = request.form.get('psw')
        user_info_creds = models.User.query.filter_by(login=user_login, password=user_password).first()
        if user_info_creds:
            session['user_name'] = user_login
            return 'ok'
        else:
            return 'nema('






@app.get("/user/<user_id>/history")
def show_user_history(user_id):
    database.init_db()
    # res = get_data(f"SELECT * FROM 'Transaction' WHERE user='{user_id_initial}'")
    res = Transaction.query.filter_by(user_id_initial=user_id).first()
    return {'id': res.id, 'user_id_initial': res.user_id_initial, 'operation_type': res.operation_type,
            'currency_num_spent': res.currency_num_spent, 'currency_num_obtained': res.currency_num_obtained,
            'currency_name_spent': res.currency_name_spent, 'currency_name_obtained': res.currency_name_obtained,
            'date_time': res.date_time, 'user_id_final': res.user_id_final, 'commission': res.commission}


@app.get("/user/<user_id>/deposit")
def show_user_deposit(user_id):
    database.init_db()
    # res = get_data(f"SELECT * FROM Deposit WHERE user_id='{user_id}'")
    res = Deposit.query.filter_by(user_id=user_id).first()
    return {'id': res.id, 'user_id': res.user_id, 'opening_date': res.opening_date, 'closing_date': res.closing_date,
            'balance': res.balance, 'interest_rate': res.interest_rate, 'dividends_account': res.dividends_account,
            'dividends_date': res.dividends_date}


#### POST ####

@app.post("/currency/<currency_name>/review")
def add_currency_rating(currency_name):
    database.init_db()
    request_data = request.get_json()
    rating = request_data['rating']
    comment = request_data['comment']
    rating_obj = Rating(currency_name=currency_name, rating=rating, comment=comment)
    database.db_session.add(rating_obj)
    database.db_session.session.commit()
    # get_data(f"INSERT INTO Rating (currency_name, rating, comment) VALUES ('{currency_name}', {rating}, '{comment}' )")
    return 'ok'


@app.get('/test1')
def test1():
    task_obj = task1.apply_async(args=[1, 10, 20, 300])
    return str(task_obj)


@app.get("/currency/trade/<currency_name_1>/<currency_name_2>")
def init_transaction(currency_name_1, currency_name_2):
    if session.get('user_name') is not None:
        return '''
               <html>
               <form method="post">
                 <div class="container">
                   <label for="uname"><b>amount_currency</b></label>
                   <input type="text" placeholder="Enter value" name="amount_currency" required>

                   <button type="submit">Submit</button>
                 </div>
               </form>
               </html>  
               '''
    else:
        return 'login first'

@app.post("/currency/trade/<currency_name_1>/<currency_name_2>")
def exchange(currency_name_1, currency_name_2):
    #user_id = 1
    user_id = session.get('user_login')
    amount1 = float(request.form.get('amount_currency'))
    #amount1 = request.get_json()['amount']
    transaction_id = uuid.uuid4()
    database.init_db()
    transaction_queue_record = models.TransactionQueue(transaction_id=str(transaction_id), status='in queue')
    database.db_session.add(transaction_queue_record)
    database.db_session.commit()
    task_obj = task1.apply_async(args=[user_id, currency_name_1, currency_name_2, amount1, transaction_id])
    return {'task_id': str(task_obj)}


@app.teardown_appcontext
def shutdown_session(exception=None):
    database.db_session.remove()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
