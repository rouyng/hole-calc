FROM tiangolo/meinheld-gunicorn-flask:python3.8
COPY --from=ghcr.io/astral-sh/uv:0.13.10 /uv /usr/local/bin/uv
WORKDIR /app/app
ENV PORT 8080
ENV GUNICORN_CONF /app/app/gunicorn_conf.py
COPY pyproject.toml uv.lock ./
RUN uv export --frozen --no-dev --no-hashes --no-emit-project -o requirements.txt \
 && uv pip install --system --no-cache -r requirements.txt
COPY holecalc holecalc
COPY templates templates
COPY static static
COPY config config
COPY main.py forms.py gunicorn_conf.py ./
