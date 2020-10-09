import json
import requests
import logging
import os
from hashlib import sha256

from flask import render_template, redirect

from app import app, db
from app.forms import PaymentForm
from app.models import Transaction, TransactionSend
from config import URL_PIASTRIX_EN, URL_PIASTRIX_INVOICE_CRATE, URL_PIASTRIX_BILL_CRATE, SECRET_KEY, PAYWAY, SHOP_ID


CURRENCY_CODE = {
    'EUR': '978',
    'USD': '840',
    'RUB': '643',
    'UAH': '980'
}

base_path = os.path.dirname(os.path.realpath(__file__))
logfile = base_path + '/../logs/main.log'
logging.basicConfig(filename=logfile, level=logging.INFO)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = PaymentForm()
    logging.info('Login to the payment page')

    if form.validate_on_submit():

        transaction = Transaction(
            amount=form.amount.data,
            currency=form.currency.data,
            description=form.description.data
        )
        db.session.add(transaction)
        db.session.commit()

        if form.currency.data == 'EUR':

            data_for_send = {
                'amount': str(transaction.amount),
                'currency': CURRENCY_CODE.get(transaction.currency),
                'description': transaction.description,
                'shop_id': SHOP_ID,
                'shop_order_id': str(transaction.id),
            }

            keys = ['amount', 'currency', 'shop_id', 'shop_order_id']
            sign = create_sign(keys, data_for_send)
            data_for_send.update({'sign': sign})

            transaction_send = TransactionSend(
                transaction_id=transaction.id,
                request=str(data_for_send),
                response=None
            )
            db.session.add(transaction_send)
            db.session.commit()

            logging.info(f'Запрос: {data_for_send}')

            return render_template('direct.html', data=data_for_send, url_=URL_PIASTRIX_EN)

        elif form.currency.data == 'USD':

            headers = {'Content-Type': 'application/json'}
            data_for_send = {
                "payer_currency": CURRENCY_CODE.get(transaction.currency),
                "shop_amount": str(transaction.amount),
                "shop_currency": CURRENCY_CODE.get(transaction.currency),
                "shop_id": SHOP_ID,
                "shop_order_id": str(transaction.id),
            }

            keys = ['shop_amount', 'shop_currency', 'shop_id', 'shop_order_id', 'payer_currency']
            sign = create_sign(keys, data_for_send)
            data_for_send.update({'sign': sign})

            logging.info(f'Запрос: {data_for_send}')

            try:
                response_json = requests.post(URL_PIASTRIX_BILL_CRATE, json=data_for_send, headers=headers)
            except Exception as e:
                logging.error(f'Ошибка сети. Ошибка: {e}')
                return

            if not response_json:
                logging.error('Провайдер вернул пустой ответ, или возникла ошибка обработке ответа провайдера')
                return

            response = json.loads(response_json.content)

            logging.info(f'Ответ: {response}')

            transaction_send = TransactionSend(
                transaction_id=transaction.id,
                request=str(data_for_send),
                response=str(response)
            )
            db.session.add(transaction_send)
            db.session.commit()

            if not response.get('result'):
                logging.error('В ответе провайдера нет поля "result"')
                return

            url = response.get('data', {}).get('url')

            return redirect(url, code=302)

        elif form.currency.data == 'RUB':

            headers = {'Content-Type': 'application/json'}
            data_for_send = {
                "amount": str(transaction.amount),
                "currency": CURRENCY_CODE.get(transaction.currency),
                "payway": PAYWAY,
                "shop_id": SHOP_ID,
                "shop_order_id": str(transaction.id),
            }

            keys = ['amount', 'currency', 'payway', 'shop_id', 'shop_order_id']
            sign = create_sign(keys, data_for_send)
            data_for_send.update({'sign': sign})

            logging.info(f'Запрос: {data_for_send}')

            try:
                response_json = requests.post(URL_PIASTRIX_INVOICE_CRATE, json=data_for_send, headers=headers)
            except Exception as e:
                logging.error(f'Ошибка сети. Ошибка: {e}')
                return

            if not response_json:
                logging.error('Провайдер вернул пустой ответ, или возникла ошибка обработке ответа провайдера')
                return

            response = json.loads(response_json.content)

            logging.info(f'Ответ: {response}')

            transaction_send = TransactionSend(
                transaction_id=transaction.id,
                request=str(data_for_send),
                response=str(response)
            )
            db.session.add(transaction_send)
            db.session.commit()

            if not response.get('result'):
                logging.error('В ответе провайдера нет поля "result"')
                return

            return render_template('invoice.html',
                                   method_=response.get('data', {}).get('method'),
                                   url=response.get('data', {}).get('url'),
                                   data=response.get('data', {}).get('data'),)

    return render_template('index.html', title='Home', form=form)


def create_sign(keys, data):
    lst = []

    for key in sorted(keys):
        lst.append(data.get(key))
    data_sing = ':'.join(lst) + SECRET_KEY

    sign = sha256(data_sing.encode()).hexdigest()
    return sign
