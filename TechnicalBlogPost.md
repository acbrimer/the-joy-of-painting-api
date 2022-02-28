# Using Google Cloud Run for Read-Only Relational Data

## Goal

A couple weeks ago, I started toying around with the idea of using Google’s Cloud Run service to deploy a Flask API packaged with a small, read-only sqlite3 database. A Google search with any combination of the terms “database” and “Google Cloud Run” will quickly show that, while doable, it is unwise to try and use Cloud Run for hosting a fully-functional relational database (see this Stack Overflow answer). Essentially, Cloud Run does not allow a good option for deploying containers that need to do anything involving persisted writes to the filesystem within the container. This makes sense as there are several other Google Cloud Services that are much better suited for projects that require a relational database (Cloud SQL, BigQuery, Compute Engine), however, these options can be overkill for use cases requiring a small, read-only set of relational data.

With these considerations, I wanted to see if it was 1) possible, and 2) practical to deploy a container with a “baked-in”, sqlite3 .db file.

## Project

For my initial test, I used a project I completed for one of my (most fun so-far) Holberton web carriculum in which the task was to build a database and API against data on episodes of The Joy of Painting. 
