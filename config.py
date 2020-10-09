import os


URL_PIASTRIX_EN = 'https://pay.piastrix.com/en/pay'
URL_PIASTRIX_BILL_CRATE = 'https://core.piastrix.com/bill/create'
URL_PIASTRIX_INVOICE_CRATE = 'https://core.piastrix.com/invoice/create'
SECRET_KEY = 'SecretKey01'
PAYWAY = 'payeer_rub'
SHOP_ID = '5'

base_path = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '@&GR@(R()HCHSC)FWEFHWGFC(GS'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(base_path, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
