# Pull base image
FROM python:3.6-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# install required packages
RUN apt-get update && apt-get install -y git python3-dev libpq-dev build-essential

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./docker/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./docker/django/start.sh /start.sh
RUN sed -i 's/\r//' /start.sh
RUN chmod +x /start.sh

# Copy project
COPY . .

ENTRYPOINT ["/entrypoint.sh"]