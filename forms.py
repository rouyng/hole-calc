"""Module that defines forms used in hole calc's three pin, reverse and pin size calculators.
 Forms are composed here using WTForms and Flask-WTF"""

from flask_wtf import FlaskForm
from wtforms import DecimalField, RadioField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class PinSizeDecimal(DecimalField):
    """Defines pin gage diameter input fields"""
    def __init__(self, pin_number: int, **kwargs):
        super().__init__(
            label=f'Pin {pin_number}',
            validators=[DataRequired(),
                        NumberRange(min=0.00001,
                                    max=9999,
                                    message="Input value must be at least %(min)s")],
            **kwargs
        )


class PinClassSelect(SelectField):
    """Defines drop-down selection fields for pin gage tolerance classes"""
    def __init__(self, pin_number: int, **kwargs):
        super().__init__(
            label=f'Pin {pin_number} Class',
            choices=[
                ('ZZ', 'ZZ'),
                ('Z', 'Z'),
                ('Y', 'Y'),
                ('X', 'X'),
                ('XX', 'XX'),
            ],
            default='ZZ',
            **kwargs

        )


class PinSignSelect(SelectField):
    """Defines drop-down selection fields for pin gage class sign (plus or minus)"""
    def __init__(self, pin_number: int, **kwargs):
        super().__init__(
            label=f'Pin {pin_number} Sign',
            choices=[
                ('+', '+'),
                ('-', '-')
            ],
            default='-',
            **kwargs
        )


class ThreePinForm(FlaskForm):
    """Defines input form for three pin bore diameter calculator"""
    tol_radio = RadioField(
        label='Tolerance',
        choices=[
            ('nom', 'Nominal'),
            ('tol', 'Tolerance')
        ],
        default='nom'
    )
    pin1 = PinSizeDecimal(1)
    pin2 = PinSizeDecimal(2)
    pin3 = PinSizeDecimal(3)
    pin1_class = PinClassSelect(1)
    pin2_class = PinClassSelect(2)
    pin3_class = PinClassSelect(3)
    pin1_sign = PinSignSelect(1)
    pin2_sign = PinSignSelect(2)
    pin3_sign = PinSignSelect(3)
    units = SelectField(
        label='Units',
        choices=[
            ('in', 'IN'),
            ('mm', 'MM')
        ]
    )
    precision = SelectField(
        label='Precision',
        choices=[
            ('0.1', '0.1'),
            ('0.01', '0.01'),
            ('0.001', '0.001'),
            ('0.0001', '0.0001'),
        ],
        default='0.001'
    )
    calculate = SubmitField('Calculate')


class ReverseForm(FlaskForm):
    """Defines input form for two pin/reverse calculator"""
    pin1 = PinSizeDecimal(1)
    pin2 = PinSizeDecimal(2)
    bore = DecimalField(label='Bore', validators=[DataRequired()])
    units = SelectField(
        label='Units',
        choices=[
            ('in', 'IN'),
            ('mm', 'MM')
        ]
    )
    precision = SelectField(
        label='Precision',
        choices=[
            ('0.1', '0.1'),
            ('0.01', '0.01'),
            ('0.001', '0.001'),
            ('0.0001', '0.0001'),
        ],
        default='0.001'
    )
    calculate = SubmitField('Calculate')


class PinSizeForm(FlaskForm):
    """Defines input form for gage pin diameter calculator"""
    pin_dia = PinSizeDecimal(1)
    pin_class = PinClassSelect(1)
    pin_sign = PinSignSelect(1)
    units = SelectField(
        label='Units',
        choices=[
            ('in', 'IN'),
            ('mm', 'MM')
        ]
    )
    calculate = SubmitField('Calculate')
