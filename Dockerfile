FROM python:3.11

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app/pkg

RUN pip install poetry==2.1.2

COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi
COPY sample_data /app/pkg/sample_data
COPY src /app/pkg/src
COPY streamlit_app.py ./

ENV HOST=0.0.0.0 \
    PORT=80 \
    APP=src.app:app

CMD uvicorn $APP --host $HOST --port $PORT

