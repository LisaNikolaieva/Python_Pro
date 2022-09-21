from sqlalchemy import Column, Integer, String, REAL, Text
from database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship



class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    balance = Column(REAL, nullable=False)
    currency_name = Column(String(20), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'balance': self.balance,
            'currency_name': self.currency_name
        }


class Currency(Base):
    __tablename__ = 'currency'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(20), nullable=False)
    USD_relative_value = Column(REAL, nullable=False)
    available_quantity = Column(REAL, nullable=False)
    date = Column(String(20), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'USD_relative_value': self.USD_relative_value,
            'available_quantity': self.available_quantity,
            'date': self.date
        }


class Deposit(Base):
    __tablename__ = 'deposit'
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    opening_date = Column(String(20), nullable=False)
    closing_date = Column(String(20))
    balance = Column(REAL, nullable=False)
    interest_rate = Column(REAL, nullable=False)
    dividends_account = Column(String(20), nullable=False)
    dividends_date = Column(String(20), nullable=False)

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


class Rating(Base):
    __tablename__ = 'rating'
    id = Column(Integer, primary_key=True, nullable=False)
    currency_name = Column(String(20), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String(50))

    def to_dict(self):
        return {
            'id': self.id,
            'currency_name': self.currency_name,
            'rating': self.rating,
            'comment': self.comment
        }


class Transaction(Base):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True, nullable=False)
    user_id_initial = Column(Integer)
    operation_type = Column(String(60))
    currency_num_spent = Column(REAL)
    currency_num_obtained = Column(REAL)
    currency_name_spent = Column(String(20))
    currency_name_obtained = Column(String(20))
    date_time = Column(String(20))
    user_id_final = Column(Integer)
    commission = Column(REAL)

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


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, nullable=False)
    login = Column(String(20), nullable=False)
    password = Column(String(20), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'login': self.login,
            'password': self.password
        }


class TransactionQueue(Base):
    __tablename__ = 'TransactionQueue'
    id = Column(Integer, primary_key=True, nullable=False)
    transaction_id = Column(String(60), nullable=False)
    status = Column(String(60), nullable=False)
