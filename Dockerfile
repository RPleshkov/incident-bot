FROM python:3.13-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /email_worker

RUN pip install --upgrade pip && \
    pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.in-project true && \
    poetry install --no-root --no-interaction --no-ansi && \
    rm -rf ~/.cache

COPY . .

CMD ["poetry", "run", "python", "main.py"]