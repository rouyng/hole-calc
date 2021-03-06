"""Module containing flask routes for holecalc web app"""

from flask import Flask, render_template, request, flash
from holecalc import holecalc as hc
from decimal import Decimal
import logging
from forms import ThreePinForm, ReverseForm, PinSizeForm
from flask_wtf.csrf import CSRFProtect
from wtforms import ValidationError
import copy
import os

app = Flask(__name__)
csrf = CSRFProtect(app)


def load_config(mode=os.environ.get('FLASK_ENV')):
    if mode == 'production':
        logging.info("Loading production environment config")
        from config import prod
        app.config.from_object(prod)
    elif mode == 'testing':
        logging.info("Loading test environment config")
        from config import test
        app.config.from_object(test)
    else:
        logging.info("Loading development environment config")
        from config import dev
        app.config.from_object(dev)


load_config()


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
    """Route for about page"""
    return render_template('about.html')


@app.route('/guide/')
def guide():
    """Route for guide page"""
    return render_template('guide.html')


@app.route('/', methods=('GET', 'POST'))
def three_pin_calc_render():
    """Route for home page containing three pin calculator"""
    form = ThreePinForm()
    calc_menu = copy.deepcopy(default_calc_menu)
    calc_menu['Three Pin']['selected'] = True
    if request.method == 'POST':
        logging.info("POST request from user on three pin calculator")
        if not form.validate_on_submit():
            flash('Form validation failed')
            logging.warning("Form validation failed")
            return render_template(
                'threepin.html',
                form=form,
                calc_menu=calc_menu
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
        tol_type = form.tol_radio.data
        if tol_type == 'nom':
            logging.info(f"Calculating hole size in nominal mode, pins: {pin1}, {pin2}, {pin3}")
            calc_result = hc.calculate_hole_size(pin1, pin2, pin3)
            try:
                if calc_result['error'] is not None:
                    raise ValueError(calc_result['error'])
                formatted_result = str(calc_result['result'].quantize(Decimal(precision)))
                logging.info(f"Calculated hole size in nominal mode: {formatted_result}")
                flash('Diameter: ' + formatted_result)
            except (TypeError, ValueError) as e:
                logging.info(f"Calculation error generated during hole size calculation: {str(e)}")
                flash(str(e))
        else:
            try:
                logging.info(f"Calculating hole size in tolerance mode, pins: "
                             f"{pin1}, {pin2}, {pin3}")
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
                max_result = str(max(result_values))
                min_result = str(min(result_values))
                logging.info(f"Calculated hole size in tolerance mode, min: {min_result}, "
                             f"max: {max_result}")
                flash(f'Min diameter: {min_result} {form_units}')
                flash(f'Max diameter: {max_result} {form_units}')
            except (TypeError, ValueError) as e:
                logging.info(f"Calculation error generated during hole size calculation: {str(e)}")
                flash(str(e))
    return render_template('threepin.html',
                           form=form,
                           calc_menu=calc_menu)


@app.route('/pinsize', methods=('GET', 'POST'))
def pin_calc_render():
    """Route for pin size calculator"""
    form = PinSizeForm()
    calc_menu = copy.deepcopy(default_calc_menu)
    calc_menu['Gage Size']['selected'] = True
    if request.method == 'POST':
        logging.info("POST request from user on pin size calculator")
        if not form.validate_on_submit():
            logging.warning("Form validation failed")
            flash('Form validation failed')
            return render_template(
                'reverse.html',
                form=form
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
            logging.info(f"Calculating pin size, nominal: {pin_dia} class: {pin_class} "
                         f"{form.pin_sign.data}")
            calc_result = hc.pin_size_wrapper(w_nominal=pin_dia,
                                              w_units=form_units,
                                              w_is_plus=pin_is_pos,
                                              w_tol_class=pin_class)
            if calc_result['result'] is None:
                logging.info(f"Calculation error generated during pin size calculation: "
                             f"{calc_result['error']}")
                flash(calc_result['error'])
            else:
                result_values = (calc_result['result'][0].quantize(Decimal(precision)),
                                 calc_result['result'][1].quantize(Decimal(precision)))
                min_result = str(min(result_values))
                max_result = str(max(result_values))
                logging.info(f"Calculated pin size, min: {min_result} max: {max_result}")
                flash(f'Min gage diameter: {min_result} {form_units}')
                flash(f'Max gage diameter: {max_result} {form_units}')
    return render_template('pinsize.html',
                           form=form,
                           calc_menu=calc_menu)


@app.route('/reverse', methods=('GET', 'POST'))
def reverse_calc_render():
    """Route for reverse/two pin calculator"""
    form = ReverseForm()
    calc_menu = copy.deepcopy(default_calc_menu)
    calc_menu['Reverse']['selected'] = True
    if request.method == 'POST':
        logging.info("POST request from user on reverse calculator")
        try:
            form.validate()
        except ValidationError as e:
            logging.warning(f"Form validation failed: {e}")
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
            logging.info(f"Calculation error generated during reverse calculation: "
                         f"{calc_result['error']}")
            flash(calc_result['error'])
        else:
            formatted_result = str(calc_result['result'].quantize(Decimal(precision)))
            logging.info(f"Calculated pin size in reverse mode: {formatted_result}")
            flash(f'Diameter: {formatted_result} {form_units}')
    return render_template('reverse.html',
                           form=form,
                           calc_menu=calc_menu)


if __name__ == '__main__':

    app.run(debug=True)
