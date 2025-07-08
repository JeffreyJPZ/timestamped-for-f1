FROM python:3.13 AS builder

COPY --from=ghcr.io/astral-sh/uv:0.7.19 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1

ENV UV_LINK_MODE=copy

# Install dependencies
WORKDIR /timestamped_for_f1_historical_api
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Install source code
COPY . /timestamped_for_f1_historical_api
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev


FROM python:3.13

COPY --from=builder --chown=timestamped_for_f1_historical_api:timestamped_for_f1_historical_api \
    /timestamped_for_f1_historical_api /timestamped_for_f1_historical_api

ENV PATH="/timestamped_for_f1_historical_api/.venv/bin:$PATH"

CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8888"]

