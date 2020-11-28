from flask import Flask, render_template, request
from holecalc import holecalc as hc
from decimal import Decimal, InvalidOperation
import logging
from forms import ThreeHoleForm
from flask_wtf.csrf import CSRFProtect
import os
from config import Config

app = Flask(__name__)
# import config settings (key) from config.py module
app.config.from_object(Config)
# set CSRF protection globally on app
csrf = CSRFProtect(app)
# Set logging level to show INFO-level or higher
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@app.route('/about.html')
def about():
    return render_template('about.html')


@app.route('/guide.html')
def guide():
    return render_template('guide.html')


@app.route('/', methods=('GET', 'POST'))
def home_calc():
    form = ThreeHoleForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template(
                '3hole.html',
                form=form,
                error='Form validation failed'
            )
        form_units = form.units.data
        precision = form.precision.data
        pin1 = form.pin1.data
        pin1_class = form.pin1_class.data
        pin2_is_pos = form.pin1_sign.data == '+'
        pin2 = form.pin2.data
        pin2_class = form.pin2_class.data
        pin3_is_pos = form.pin2_sign.data == '+'
        pin3 = form.pin3.data
        pin3_class = form.pin3_class.data
        pin1_is_pos = form.pin3_sign.data == '+'
        rounded_result = None
        calc_error = None
        tol_type = form.tol_radio.data
        if tol_type == 'nom':
            calc_result = hc.calculate_hole_size(pin1, pin2, pin3)
            try:
                if calc_result['error'] is not None:
                    raise ValueError(calc_result['error'])
                rounded_result = calc_result['result'].quantize(Decimal(precision))
            except (TypeError, ValueError) as e:
                calc_error = e
        else:
            try:
                calc_result = hc.calculate_hole_size_limits(
                    (pin1, pin1_class, pin1_is_pos),
                    (pin2, pin2_class, pin2_is_pos),
                    (pin3, pin3_class, pin3_is_pos),
                    units=form_units
                )
                for r in calc_result:
                    if r['error'] is not None:
                        raise ValueError(r['error'])
                rounded_result = str(calc_result[0]['result'].quantize(Decimal(precision)))\
                    + ' - ' + str(calc_result[1]['result'].quantize(Decimal(precision)))
            except (TypeError, ValueError) as e:
                calc_error = e
    else:
        calc_error = None
        rounded_result = None

    return render_template('3hole.html',
                           form=form,
                           error=calc_error,
                           result=rounded_result)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    app.run(debug=True)
