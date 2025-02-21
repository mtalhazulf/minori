FROM python:3.9-slim as build

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1
ENV \
    POETRY_VERSION=1.6.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt update \
    && apt install --no-install-recommends -y \
    curl \
    build-essential

RUN curl -sSL https://install.python-poetry.org | python3

WORKDIR /app

COPY ./ ./

RUN poetry build --format wheel


FROM python:3.9-slim
WORKDIR /app
COPY --from=build /app/dist/*.whl ./
RUN pip install ./*.whl
RUN rm ./*.whl
ENV PORT=8080
ENV API__WORKERS=1
EXPOSE $PORT
ENTRYPOINT gunicorn --bind=0.0.0.0:$PORT  --workers 1 'api:create_app()'
