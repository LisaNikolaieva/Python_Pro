from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    balance = db.Column(db.REAL, nullable=False)
    currency_name = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'balance': self.balance,
            'currency_name': self.currency_name
        }


class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    USD_relative_value = db.Column(db.REAL, nullable=False)
    available_quantity = db.Column(db.REAL, nullable=False)
    date = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'USD_relative_value': self.USD_relative_value,
            'available_quantity': self.available_quantity,
            'date': self.date
        }


class Deposit(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    opening_date = db.Column(db.String(20), nullable=False)
    closing_date = db.Column(db.String(20))
    balance = db.Column(db.REAL, nullable=False)
    interest_rate = db.Column(db.REAL, nullable=False)
    dividends_account = db.Column(db.String(20), nullable=False)
    dividends_date = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'opening_date': self.opening_date,
            'closing_date': self.closing_date,
            'balance': self.balance,
            'interest_rate': self.interest_rate,
            'dividends_account': self.dividends_account,
            'dividends_date': self.dividends_date
        }


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    currency_name = db.Column(db.String(20), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(50))

    def to_dict(self):
        return {
            'id': self.id,
            'currency_name': self.currency_name,
            'rating': self.rating,
            'comment': self.comment
        }


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id_initial = db.Column(db.Integer)
    operation_type = db.Column(db.String(60))
    currency_num_spent = db.Column(db.REAL)
    currency_num_obtained = db.Column(db.REAL)
    currency_name_spent = db.Column(db.String(20))
    currency_name_obtained = db.Column(db.String(20))
    date_time = db.Column(db.String(20))
    user_id_final = db.Column(db.Integer)
    commission = db.Column(db.REAL)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id_initial': self.user_id_initial,
            'operation_type': self.operation_type,
            'currency_num_spent': self.comment,
            'currency_num_obtained': self.currency_num_obtained,
            'date_time': self.date_time,
            'user_id_final': self.user_id_final,
            'commission': self.commission

        }


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    login = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'login': self.login,
            'password': self.password
        }
