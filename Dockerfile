FROM tiangolo/meinheld-gunicorn-flask:python3.8
WORKDIR /app/app
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
# "Activate" venv by changing path
# See https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV VIRTUAL_ENV=/app/app/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt
COPY holecalc holecalc
COPY templates templates
COPY static static
COPY main.py config.py forms.py ./
