# Using Google Cloud Run for Read-Only Relational Data

## Goal

A couple weeks ago, I started toying around with the idea of using Google’s Cloud Run service to deploy a Flask API packaged with a small, read-only sqlite3 database. A Google search with any combination of the terms “database” and “Google Cloud Run” will quickly show that, while doable, it is unwise to try and use Cloud Run for hosting a fully-functional relational database (see this Stack Overflow answer). Essentially, Cloud Run does not allow a good option for deploying containers that need to do anything involving persisted writes to the filesystem within the container. This makes sense as there are several other Google Cloud Services that are much better suited for projects that require a relational database (Cloud SQL, BigQuery, Compute Engine), however, these options can be overkill for use cases requiring a small, read-only set of relational data.

With these considerations, I wanted to see if it was 1) possible, and 2) practical to deploy a container with a “baked-in”, sqlite3 .db file.

## Project

For my initial test, I used a project I completed for one of my (most fun so-far) Holberton web carriculum in which the task was to build a database and API against data on episodes of The Joy of Painting ([see here for the GitHub repo](https://github.com/acbrimer/the-joy-of-painting-api)).

Here is the database design I chose for storing the episode data from The Joy of Painting that we were given to work with:

![ER-diagram](https://github.com/acbrimer/the-joy-of-painting-api/blob/main/db_schema.png?raw=true)

After loading the `dev.db` sqlite3 database and ensuring the API was working on my laptop, I simply added the following Dockerfile from Google Cloud Run documentation into my project repository:

```
# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.10-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
```
