from datetime import datetime

from app import db


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.now())
    amount = db.Column(db.Integer)
    currency = db.Column(db.String(10))
    description = db.Column(db.Text)

    def __repr__(self):
        return '<Transaction: id {}, amount {}>'.format(self.id, self.amount)


class TransactionSend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request = db.Column(db.Text)
    response = db.Column(db.Text)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'))
