"""Module that defines forms used in hole calc's three pin, reverse and pin size calculators.
 Forms are composed here using WTForms and Flask-WTF"""

from flask_wtf import FlaskForm
from wtforms import DecimalField, RadioField, SelectChoice, SelectField, SubmitField
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
                SelectChoice('ZZ'),
                SelectChoice('Z'),
                SelectChoice('Y'),
                SelectChoice('X'),
                SelectChoice('XX'),
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
                SelectChoice('+'),
                SelectChoice('-')
            ],
            default='-',
            **kwargs
        )


class ThreePinForm(FlaskForm):
    """Defines input form for three pin bore diameter calculator"""
    tol_radio = RadioField(
        label='Tolerance',
        choices=[
            SelectChoice('nom', 'Nominal'),
            SelectChoice('tol', 'Tolerance')
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
            SelectChoice('in', 'IN'),
            SelectChoice('mm', 'MM')
        ]
    )
    precision = SelectField(
        label='Precision',
        choices=[
            SelectChoice('0.1'),
            SelectChoice('0.01'),
            SelectChoice('0.001'),
            SelectChoice('0.0001'),
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
            SelectChoice('in', 'IN'),
            SelectChoice('mm', 'MM')
        ]
    )
    precision = SelectField(
        label='Precision',
        choices=[
            SelectChoice('0.1'),
            SelectChoice('0.01'),
            SelectChoice('0.001'),
            SelectChoice('0.0001'),
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
            SelectChoice('in', 'IN'),
            SelectChoice('mm', 'MM')
        ]
    )
    calculate = SubmitField('Calculate')
