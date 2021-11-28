FROM docker.io/python:3.9-alpine

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000/tcp
VOLUME ["/app/database"]

# Configure time as Central European Time
ENV TIME_ZONE CET

# WARNING OVERWRITE THESE ENVIRONMENT VARIABLES !
ENV SECRET_KEY b2038d34-a781-4c99-8c30-c62664f9ab77
ENV DEBUG 1

CMD "./entrypoint.sh"
