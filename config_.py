import os


URL_PIASTRIX_EN = '<url>'
URL_PIASTRIX_BILL_CRATE = '<url>'
URL_PIASTRIX_INVOICE_CRATE = '<url>'
SECRET_KEY = '<SECRET_KEY>'
PAYWAY = '<PAYWAY>'
SHOP_ID = '<SHOP_ID>'

base_path = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '@&GR@(R()HCHSC)FWEFHWGFC(GS'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(base_path, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
