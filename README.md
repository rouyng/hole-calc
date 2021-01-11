[![website status shield](https://img.shields.io/website?down_message=offline&up_message=online&url=https%3A%2F%2Fholecalc.com%2Fheartbeat)](https://holecalc.com/) ![GitHub Workflow Status](https://img.shields.io/github/workflow/status/rouyng/hole-calc/test%20and%20lint?label=test%20and%20lint) ![GitHub](https://img.shields.io/github/license/rouyng/hole-calc)
# [Hole Calc](https://holecalc.com)

Hole calc is a simple web application that allows you to calculate the diameter of a bore from the size of three cylindrical pin gages that fit into it, using [Descartes' Theorem](https://en.wikipedia.org/wiki/Descartes%27_theorem). This functionality is useful for machinists and anyone else who needs a semi-precision method of measuring bore diameters without dedicated tools. See the [guide](https://holecalc.com/guide) for more info on how to use hole calc.

## Application structure
The holecalc application is built with the [Flask](https://flask.palletsprojects.com/en/1.1.x/) web application microframework. [Flask-WTForms](https://flask-wtf.readthedocs.io/en/stable/) was used to build the form. The source code for the flask app is contained in `main.py`, while Flask templates reside in the `templates` subdirectory.

The holecalc module contains the backend code that runs the geometry calculations for the application's main functionality. This module also contains a couple placeholder functions that need to be completed for future planned features (see TODO section below).

## Styling
Hole calc is styled using [Pure.css](https://purecss.io/). The display font used for the menu and headings is [Space Grotesk](https://fonts.floriankarsten.com/space-grotesk) by Florian Karsten. The color scheme may be viewed [here](https://coolors.co/191d32-4d7ea8-b6c2d9-ffc857-ba2c73).

## Build, test and deployment
Hole calc is developed and tested using Python 3.8. A pipfile is included for dependency management with Pipenv.

The preferred way to build and deploy this application is via Docker, using the included Dockerfile. The base image used is `tiangolo/meinheld-gunicorn-flask:python3.8` ([docs](https://github.com/tiangolo/meinheld-gunicorn-flask-docker)).

Automated tests for the pytest framework are found in the `tests` subdirectory. Tests and linting with flake8 are run via GitHub action on every push to the master branch of this repository.

## TODO:
* Use html SVG rendering to draw the three input diameters and the output diameter. While hole calc can currently determine all these diameters, finding the formula to calculate relative position of the circle centers is difficult with my mediocre geometry skills. If you can assist with the geometry involved, please contact me!
* Improve guide page to describe "reverse" and "gage size" calculators

## Contributing
Bug reports, feature suggestions and code contributions are welcome. You may open an issue or pull request through GitHub or by contacting me directly through the contact information listed on my GitHub profile.

## License
Hole calc is licensed according to the terms of the MIT license. See LICENSE.md for details.
