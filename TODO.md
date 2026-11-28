# TODO: dependency and tooling modernization

Handoff notes for continuing this work in a new session. Last updated 2026-11-27.

## Done

- **Phase 1: Pipenv → uv** (PR #45). `pyproject.toml` + `uv.lock`, dev tools in the `dev` dependency group, CI on `astral-sh/setup-uv` with `uv sync --locked`.
- **Phase 2.1 + 2.2: Python 3.15 and dependency upgrades** (PR #47). These had to land together: the old pins broke on every Python ≥3.12 (bs4 4.9.3 lost its html5lib builder; Jinja2 2.11 used `ast.Str`, removed in 3.14).
  - Flask 3.1, Werkzeug 3.1, Jinja2 3.1, Flask-WTF 1.3, WTForms 3.3, pytest 9.2, flake8 7.5, gunicorn 27.
  - `forms.py` uses `wtforms.SelectChoice` instead of tuples.
  - Docker: `python:3.15-slim-trixie`, `uv sync --frozen --no-dev`, gunicorn as non-root user, app in `/app`.
  - Env var `FLASK_ENV` renamed to `APP_ENV`, with no fallback.
- **gunicorn timeout 1000s → 30s, `graceful_timeout = 30`** (commit `bbe8522` on master).

## Deployment (maintainer)

- [ ] Set `APP_ENV=production` on the server. **If it's unset, the app starts without error on the development config**: `DEBUG=True`, CSRF off, placeholder `SECRET_KEY`.
- [ ] After deploying, watch the logs for `WORKER TIMEOUT`. If it shows up, fix the heartbeat or slow-request cause rather than raising `timeout`.
- [ ] Optional: temporarily add `access_log_format = '%(h)s "%(r)s" %(s)s %(b)s %(M)sms'` to `gunicorn_conf.py` to confirm real request durations sit far below 30s.

## Phase 2.3: test and lint cleanup

- [ ] Replace flake8 with ruff:
  - Add `ruff` to the `dev` group and `[tool.ruff]` with `line-length = 100`.
  - Delete `.flake8`.
  - Run `ruff check` and `ruff format --check` in `.github/workflows/ci.yml`.
- [ ] Fix the existing lint warnings (from `flake8 --max-line-length=100 --max-complexity=10`):
  - `holecalc/holecalc.py:6`: unused imports `acos, cos, radians, degrees, sqrt` from `math`.
  - `holecalc/holecalc.py:280`: f-string with no placeholders.
  - `main.py:254/261/268`: the 404, 403 and 500 error handlers are all named `page_not_found` (F811). They work, because the decorators register each one before it's redefined, but they should have distinct names.
  - 5× E128 continuation-line indentation and 3× E402 import-not-at-top.
  - C901 complexity 11 in `pin_tolerance_limits` and `three_pin_calc_render`. Refactoring is optional; it could also be accepted with a raised threshold.
- [ ] Make CI fail on all lint errors once the code is clean. It currently uses `--exit-zero` for the style checks.
- [ ] Delete `tests/context.py`. No test imports it; the tests resolve `main` and `holecalc` through pytest's rootdir handling. Add `[tool.pytest.ini_options] pythonpath = ["."]` to make that explicit.
- [ ] Add a test that `load_config("production")` raises without `SECRET_KEY`.
- [ ] Fix the flaky test, issue #46. `test_mm_small_tolerances` fails about 9% of runs: the random diameter can round to exactly 0.254 mm, which `pin_tolerance_limits` rejects (`<=` at `holecalc/holecalc.py:86`). The issue also notes that the inch and mm lower bounds disagree by a factor of 10.

## Phase 2.4: small fixes

- [ ] Fix the CI badge in `README.md` line 1. Shields.io removed the `github/workflow/status` endpoint; use `https://img.shields.io/github/actions/workflow/status/rouyng/hole-calc/ci.yml?label=test%20and%20lint`.
- [ ] Add `.github/dependabot.yml` with the `uv` ecosystem for `uv.lock` and `github-actions` for the workflows.
- [ ] Reassess `django-htmlmin`, which is barely maintained and pulls in bs4 and html5lib. It works on 3.15 today. Options: `minify-html`, or drop minification and rely on gzip at nginx.
- [ ] README cleanup: line 9 refers to placeholder functions and a TODO section that no longer apply.

## Notes for the next session

- **Memory:** the dev VM has 2.7 GiB RAM and no swap. It froze once during a multi-version `uv run` loop. Wrap installs and test runs in `systemd-run --user --scope -p MemoryMax=800M -p MemorySwapMax=0 …`. The limit is enforced on this VM. Normal test runs peak under 100 MiB.
- **Docker:** it needs `sudo`, which the agent doesn't have. The maintainer runs `docker build` / `docker run` checks.
- **Local production smoke test without Docker:** `APP_ENV=production SECRET_KEY=x PORT=8099 uv run gunicorn -c gunicorn_conf.py main:app`. Form POSTs need the `csrf_token` from a GET of the same page, with cookies kept.
