# Use the official Debian base image
FROM python:3.10-buster

# setup environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# upgrade pip
RUN pip install --upgrade pip

# copy requirements file
COPY ./requirements.txt /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libmariadb-dev-compat \
    libmariadb-dev \
    libjpeg-dev \
    zlib1g-dev \
    libffi-dev \
    netcat \
    && rm -rf /var/lib/apt/lists/*

# install python dependencies
RUN pip install -r requirements.txt

# copy whole project to your work directory
COPY . /usr/src/app

# port where the Django app runs
EXPOSE 8000

# list files for debugging
RUN ls -a

# make wait_db.sh executable
RUN chmod +x ./scripts/wait_db.sh

# entrypoint
ENTRYPOINT ["./scripts/wait_db.sh"]