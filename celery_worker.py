from celery import Celery
import datetime
import time
import models
import database
app = Celery('celery_worker', broker='pyamqp://guest@localhost//')




@app.task
def task1(user_id, currency_name_1, currency_name_2, amount1, transaction_id):
    # print(user_id, currency_name_1, currency_name_2,amount1)
    # return True
    database.init_db()
    transaction_record = models.TransactionQueue.query.filter_by(transaction_id=transaction_id).first()
    date_now = datetime.datetime.now().strftime('%d.%m.%Y')
    commission = 0.2 * amount1
    amount1c = amount1 + commission

    user_balance1 = models.Account.query.filter_by(user_id=user_id, currency_name=currency_name_1).first().balance
    user_balance2 = models.Account.query.filter_by(user_id=user_id, currency_name=currency_name_2).first().balance

    cur1_USD_relative_value = models.Currency.query.filter_by(name=currency_name_1, date=date_now).first().USD_relative_value
    cur2_USD_relative_value = models.Currency.query.filter_by(name=currency_name_2, date=date_now).first().USD_relative_value

    need_cur2 = amount1 * cur1_USD_relative_value / cur2_USD_relative_value

    existing_amount_currency1 = models.Currency.query.filter_by(name=currency_name_1, date=date_now).first().available_quantity
    existing_amount_currency2 = models.Currency.query.filter_by(name=currency_name_2, date=date_now).first().available_quantity

    if (user_balance1 >= amount1) and (existing_amount_currency2 > need_cur2):

        models.Currency.query.filter_by(name=currency_name_2, date=date_now).update(
            dict(available_quantity=(existing_amount_currency2 - need_cur2)))
        models.Currency.query.filter_by(name=currency_name_1, date=date_now).update(
            dict(available_quantity=(existing_amount_currency1 + amount1c)))

        models.Account.query.filter_by(user_id=user_id, currency_name=currency_name_1).update(
            dict(balance=(user_balance1 - amount1c)))
        models.Account.query.filter_by(user_id=user_id, currency_name=currency_name_2).update(
            dict(balance=(user_balance2 + need_cur2)))

        transaction_obj = models.Transaction(user_id_initial=user_id, operation_type='exchange', currency_num_spent=amount1,
                                      currency_num_obtained=need_cur2, currency_name_spent=currency_name_1,
                                      currency_name_obtained=currency_name_2, date_time=date_now, user_id_final=user_id,
                                      commission=commission)
        database.db_session.add(transaction_obj)
        transaction_record.status = 'done'
        database.db_session.add(transaction_record)
        database.db_session.commit()

        return 'ok'
    else:
        return 'not ok'
