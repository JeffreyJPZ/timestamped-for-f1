FROM python:3.13 AS builder

COPY --from=ghcr.io/astral-sh/uv:0.7.19 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1

ENV UV_LINK_MODE=copy

WORKDIR /historical_api

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

COPY ./src/historical_api /historical_api

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT []

CMD ["fastapi", "run", "historical_api/main.py", "--host", "0.0.0.0", "--port", "8888"]

