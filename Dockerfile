FROM python:3.10-slim-buster as builder

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/code
ENV DEBUG=1

WORKDIR /code
EXPOSE 8000

RUN apt-get update && \
    apt-get install -y libpq-dev gcc

RUN pip install --upgrade pip && \
    pip install psycopg2 && \
    pip install poetry && \
    poetry config virtualenvs.create false

COPY ./scripts /scripts

COPY ./pyproject.toml ./poetry.lock* /code/

RUN poetry install --no-root && \
    poetry export -f requirements.txt --output requirements.txt --without-hashes

# install gdal library
RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin python-gdal python3-gdal && \
    useradd --no-create-home app && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R app:app /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts


FROM builder as development
COPY ./ /code/

ENV PATH="/scripts:/py/bin:$PATH"

USER app

CMD ["run.sh"]