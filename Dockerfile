FROM python:3.9.0b1-alpine

# add alpine packages

RUN apk update && apk add gcc

# Setup directories and copy requirements file

RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY ./requirements.txt .

# Install python packages

RUN pip install -r requirements.txt

# Copy source files

COPY ./pydock/* /usr/src/app/

# Run the app on container start

CMD python3 -u pydock.py