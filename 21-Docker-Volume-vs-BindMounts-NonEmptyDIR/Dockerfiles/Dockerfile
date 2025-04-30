# Use nginx:alpine-slim as base Docker Image
FROM nginx:alpine-slim

# OCI Labels
LABEL org.opencontainers.image.authors="Kalyan Reddy Daida"
LABEL org.opencontainers.image.title="Demo: Docker Volumes vs Bind Mounts"
LABEL org.opencontainers.image.description="Learn the Differences Between Docker Volumes and Bind Mounts When Mounted to a Non-Empty Directory in a Container"
LABEL org.opencontainers.image.version="1.0"

# Using COPY to copy a local file
COPY ./static-content/ /usr/share/nginx/html

