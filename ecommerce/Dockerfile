FROM python:3.9-alpine
RUN mkdir /ecommerce
WORKDIR /ecommerce
ADD requirements.txt .
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev \
    && pip install --upgrade pip && pip install -r requirements.txt
ADD . .