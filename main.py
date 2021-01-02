from flask import Flask, render_template, request, flash
from holecalc import holecalc as hc
from decimal import Decimal
import logging
from forms import ThreePinForm, ReverseForm, PinSizeForm
from flask_wtf.csrf import CSRFProtect
from wtforms import ValidationError
from config import DevConfig
import copy

app = Flask(__name__)
# import config settings (key) from config.py module
app.config.from_object(DevConfig)
# set CSRF protection globally on app
csrf = CSRFProtect(app)
# Set logging level to show INFO-level or higher
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

default_calc_menu = {"Three Pin": {'route': "/",
                                   'selected': False},
                     "Reverse": {'route': "/reverse",
                                 'selected': False},
                     "Gage Size": {'route': "/pinsize",
                                    'selected': False}}


@app.route('/heartbeat')
def heartbeat():
    """return an OK message for simple testing of app deployment"""
    return "OK"


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/guide/')
def guide():
    return render_template('guide.html')


@app.route('/', methods=('GET', 'POST'))
def three_pin_calc_render():
    form = ThreePinForm()
    calc_menu = copy.deepcopy(default_calc_menu)
    calc_menu['Three Pin']['selected'] = True
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Form validation failed')
            return render_template(
                'threepin.html',
                form=form,
                error=True
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
        calc_error = False
        tol_type = form.tol_radio.data
        if tol_type == 'nom':
            calc_result = hc.calculate_hole_size(pin1, pin2, pin3)
            try:
                if calc_result['error'] is not None:
                    raise ValueError(calc_result['error'])
                flash('Diameter:' + str(calc_result['result'].quantize(Decimal(precision))))
            except (TypeError, ValueError) as e:
                calc_error = True
                flash(str(e))
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
                result_values = (calc_result[0]['result'].quantize(Decimal(precision)),
                                 calc_result[1]['result'].quantize(Decimal(precision)))
                flash('Min diameter:' + str(min(result_values)))
                flash('Max diameter:' + str(max(result_values)))
            except (TypeError, ValueError) as e:
                calc_error = True
                flash(str(e))
    else:
        calc_error = False

    return render_template('threepin.html',
                           form=form,
                           error=calc_error,
                           calc_menu=calc_menu)


@app.route('/pinsize', methods=('GET', 'POST'))
def pin_calc_render():
    form = PinSizeForm()
    calc_menu = copy.deepcopy(default_calc_menu)
    calc_menu['Gage Size']['selected'] = True
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Form validation failed')
            return render_template(
                'reverse.html',
                form=form,
                error=True
            )
        else:
            form_units = form.units.data
            pin_dia = form.pin_dia.data
            pin_class = form.pin_class.data
            pin_is_pos = form.pin_sign.data == '+'
            if form_units == 'in':
                precision = "0.000001"
            else:
                precision = "0.0001"
            calc_result = hc.pin_size_wrapper(w_nominal=pin_dia,
                                              w_units=form_units,
                                              w_is_plus=pin_is_pos,
                                              w_tol_class=pin_class)
            if calc_result['result'] is None:
                calc_error = True
                flash(calc_result['error'])
            else:
                calc_error = False
                result_values = (calc_result['result'][0].quantize(Decimal(precision)),
                                 calc_result['result'][1].quantize(Decimal(precision)))
                flash('Min gage diameter:' + str(min(result_values)))
                flash('Max gage diameter:' + str(max(result_values)))

    else:
        calc_error = False

    return render_template('pinsize.html',
                           form=form,
                           error=calc_error,
                           calc_menu=calc_menu)


@app.route('/reverse', methods=('GET', 'POST'))
def reverse_calc_render():
    form = ReverseForm()
    calc_menu = copy.deepcopy(default_calc_menu)
    calc_menu['Reverse']['selected'] = True
    if request.method == 'POST':
        try:
            form.validate()
        except ValidationError as e:
            flash(str(e))
            return render_template(
                'reverse.html',
                form=form,
                calc_menu=calc_menu)
        form_units = form.units.data
        precision = form.precision.data
        pin1 = form.pin1.data
        pin2 = form.pin2.data
        bore_dia = form.bore.data
        calc_result = hc.calculate_remaining_pin(bore_dia, pin1, pin2)
        if calc_result['error'] is not None:
            flash(calc_result['error'])
        else:
            formatted_result = str(calc_result['result'].quantize(Decimal(precision)))
            flash(f'Diameter: {formatted_result} {form_units}')
    return render_template('reverse.html',
                           form=form,
                           calc_menu=calc_menu)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    app.run(debug=True)
