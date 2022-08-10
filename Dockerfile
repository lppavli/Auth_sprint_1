FROM python:3.9.12-alpine3.14

RUN apk update \
    && apk add build-base

COPY ./requirements.txt .

RUN pip install -U setuptools pip
RUN pip install -r requirements.txt

COPY . /app


WORKDIR /app

CMD ["gunicorn", "auth.pywsgi:app", "--bind", ":8000"]

# https://russianblogs.com/article/82981604616/
