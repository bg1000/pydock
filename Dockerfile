# https://rollout.io/blog/using-docker-compose-for-python-development/
# use the above to create a compose file
FROM python:3.9.0b1-alpine
RUN apk update && apk add gcc
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
# ENV PYTHONUNBUFFERED 1 <- was in example but don't think I need
COPY . .
CMD python3 -u pydock.py