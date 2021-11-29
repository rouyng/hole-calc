FROM tiangolo/meinheld-gunicorn-flask:python3.8
WORKDIR /app/app
ENV PORT 8080
ENV GUNICORN_CONF /app/app/gunicorn_conf.py
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt
COPY holecalc holecalc
COPY templates templates
COPY static static
COPY config config
COPY main.py forms.py gunicorn_conf.py ./
