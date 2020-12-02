FROM python:3.9-alpine
RUN adduser -D holes
WORKDIR /home/holes
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install pipenv
RUN venv/bin/pipenv lock --requirements > requirements.txt
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn
COPY holecalc holecalc
COPY templates templates
COPY static static
COPY app.py boot.sh config.py forms.py ./
RUN chmod a+x boot.sh
ENV FLASK_APP app.py
RUN chown -R holes:holes ./
USER holes
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]