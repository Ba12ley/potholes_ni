FROM python:3.13-slim-bookworm

WORKDIR /potholes_ni

COPY --from=ghcr.io/astral-sh/uv:0.8.14 /uv /uvx /bin/

COPY . /potholes_ni

RUN uv sync --locked
ENV PATH="/potholes_ni/.venv/bin:$PATH"
EXPOSE 8000