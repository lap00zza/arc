# Use an official Python runtime as a base image (os: alpine linux)
FROM python:3.6.1-alpine

# These packages are needed to build psycopg2 and bcrypt. Also, this line should go
# first so that changes below wont cause use to download all the packages again.
RUN apk update && apk add \
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev \
    libffi-dev

# Add requirements.txt before rest of repo, for Docker caching purposes
# See http://ilikestuffblog.com/2014/01/06/
ADD requirements.txt /api_server/

# Set the working directory to /api_server
WORKDIR api_server

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /api_server
ADD . /api_server

# We need the PYTHONUNBUFFERED environment variable to
# view the bot's output. If you want to turn it ON, just
# pass 1 when running this image.
ENV PYTHONUNBUFFERED=0
