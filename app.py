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
    return render_template('3hole.html', valid=True, input_pins=placeholder_input,
                           pins_percents=None, result="")


@app.route('/', methods=['POST'])
def post_results():
    form_input_data = request.form
    try:
        pin1 = float(form_input_data['pin1'])
        pin2 = float(form_input_data['pin2'])
        pin3 = float(form_input_data['pin3'])
        input_validated = True
    except ValueError:
        input_validated = False
        return render_template('3hole.html', valid=input_validated)
    else:
        calc_result = hc.calculate_hole_size(pin1, pin2, pin3)
        try:
            rounded_result = round(calc_result['result'], 3)
            precision = form_input_data['precision']
            round_digits = len(precision) - 2
            format_string = "{"+f":.{round_digits}f"+"}"
            if 1 < len(precision) < 5:
                rounded_result = format_string.format(round(calc_result['result'], round_digits))
        except (TypeError, ValueError):
            input_validated = False
            rounded_result = f"{calc_result['error']}"

        return render_template('3hole.html',
                               valid=input_validated,
                               input_pins=(pin1, pin2, pin3),
                               result=rounded_result)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    app.run(debug=True)
