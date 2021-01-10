from flask_wtf import FlaskForm
from wtforms import DecimalField, RadioField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class PinSizeDecimal(DecimalField):
    def __init__(self, pin_number: int, **kwargs):
        super().__init__(
            label=f'Pin {pin_number}',
            validators=[DataRequired(), NumberRange(min=0.00001, max=9999, message="Input value must be at least %(min)s")],
            **kwargs
        )


class PinClassSelect(SelectField):
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
    """
    Choose whether the pin tolerance
     class sign is positive (True) or
     negative (False)
     """

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
    """Defines the 3-pin hole measuring form"""

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
