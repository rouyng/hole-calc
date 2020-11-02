from flask import Flask, render_template, request
from holecalc import holecalc as hc
import logging

app = Flask(__name__)
# Set logging level to show INFO-level or higher
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@app.route('/about.html')
def about():
    return render_template('about.html')


@app.route('/guide.html')
def guide():
    return render_template('guide.html')


@app.route('/')
def home():
    placeholder_input = (None, None, None)
    return render_template('home.html', valid=True, input_pins=placeholder_input,
                           pins_percents=None, result="")


@app.route('/', methods=['POST'])
def post_results():
    def calc_pin_percent(pin, hole):
        radius = (round(pin / hole, 3)) * 40
        return radius

    form_input_data = request.form
    try:
        pin1 = float(form_input_data['pin1'])
        pin2 = float(form_input_data['pin2'])
        pin3 = float(form_input_data['pin3'])
    except ValueError:
        return render_template('home.html', valid=False)
    else:
        calc_result = hc.calculate_hole_size(pin1, pin2, pin3)
        rounded_result = round(calc_result, 3)
        try:
            precision = form_input_data['precision']
            round_digits = len(precision) - 2
            if 1 < len(precision) < 5:
                rounded_result = round(calc_result, round_digits)
        except ValueError:
            pass
        print(calc_pin_percent(pin2, calc_result))

        return render_template('home.html', valid=True, input_pins=(pin1, pin2, pin3),
                               pins_percent=(calc_pin_percent(pin1, calc_result),
                                             calc_pin_percent(pin2, calc_result),
                                             calc_pin_percent(pin3, calc_result)),
                               pin2_ypos= 90 - calc_pin_percent(pin2, calc_result),
                               result=rounded_result)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    app.run(debug=True)
