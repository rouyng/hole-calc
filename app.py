from flask import Flask, render_template, request
from holecalc import holecalc as hc
import logging

app = Flask(__name__)
# Set logging level to show INFO-level or higher
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/', methods=['POST'])
def post_results():
    try:
        pin1 = float(request.form['pin1'])
        pin2 = float(request.form['pin2'])
        pin3 = float(request.form['pin3'])
    except ValueError:
        return render_template('home.html', valid=False)
    else:
        calc_results = hc.calculate_hole(pin1, pin2, pin3)
        return render_template('home.html', valid=True, results=calc_results)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    app.run()
