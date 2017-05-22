# Use an official Python runtime as a base image (os: alpine linux)
FROM python:3.6.1-alpine

# Add requirements.txt before rest of repo, for Docker caching purposes
# See http://ilikestuffblog.com/2014/01/06/
ADD requirements.txt /ws_server/

# Set the working directory to /ws_server
WORKDIR ws_server

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /ws_server
ADD . /ws_server

# We need the PYTHONUNBUFFERED environment variable to
# view the bot's output. If you want to turn it ON, just
# pass 1 when running this image.
ENV PYTHONUNBUFFERED=0
