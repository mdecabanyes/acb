FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m pip install --no-cache-dir poetry==1.6.1  && poetry config virtualenvs.create false

RUN useradd -U -m acb

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install && chown -R acb:acb ./

USER acb

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
