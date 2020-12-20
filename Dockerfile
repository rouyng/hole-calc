FROM tiangolo/meinheld-gunicorn-flask:python3.8
WORKDIR /app/app
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install pipenv
RUN venv/bin/pipenv lock --requirements > requirements.txt
RUN venv/bin/pip install -r requirements.txt
COPY holecalc holecalc
COPY templates templates
COPY static static
COPY main.py config.py forms.py ./
