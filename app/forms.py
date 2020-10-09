from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


CURRENCY_DATA = [
    ("EUR", "EUR"),
    ("USD", "USD"),
    ("RUB", "RUB"),
]


class PaymentForm(FlaskForm):
    amount = IntegerField('Amount', validators=[DataRequired()])
    currency = SelectField('Currency', choices=CURRENCY_DATA)
    description = TextAreaField('Description')
    submit = SubmitField('Pay')
