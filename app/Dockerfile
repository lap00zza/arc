# Use an official Python runtime as a base image (os: alpine linux)
FROM python:3.6.1-alpine

# Add requirements.txt before rest of repo, for Docker caching purposes
# See http://ilikestuffblog.com/2014/01/06/
ADD requirements.txt /app/

# Set the working directory to /api_server
WORKDIR app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /api_server
ADD . /app

# We need the PYTHONUNBUFFERED environment variable to
# view the bot's output. If you want to turn it ON, just
# pass 1 when running this image.
ENV PYTHONUNBUFFERED=0
