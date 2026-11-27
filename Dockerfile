FROM python:3.15-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:0.13.10 /uv /usr/local/bin/uv

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    PATH="/app/.venv/bin:$PATH" \
    PORT=8080

WORKDIR /app

# Install locked runtime dependencies first so this layer is cached across code changes
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --frozen --no-dev

COPY holecalc holecalc
COPY templates templates
COPY static static
COPY config config
COPY main.py forms.py gunicorn_conf.py ./

RUN useradd --system --no-create-home app
USER app

EXPOSE 8080
CMD ["gunicorn", "-c", "gunicorn_conf.py", "main:app"]
