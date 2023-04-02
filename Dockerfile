FROM python:3.9

RUN apt-get update && apt-get install -y cmake python3-pip python3-dev

RUN mkdir /hack_the_future_api
WORKDIR /hack_the_future_api

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

COPY pyproject.toml /hack_the_future_api/
RUN pip install poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY ./app /hack_the_future_api/app
COPY ./alembic /hack_the_future_api/alembic
COPY ./alembic.ini /hack_the_future_api/alembic.ini
COPY ./main.py /hack_the_future_api/

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]