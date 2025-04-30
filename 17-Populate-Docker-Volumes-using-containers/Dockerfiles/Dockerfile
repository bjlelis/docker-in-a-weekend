# Use nginx:alpine-slim as base Docker Image
FROM nginx:alpine-slim

# OCI Labels
LABEL org.opencontainers.image.authors="Kalyan Reddy Daida"
LABEL org.opencontainers.image.title="Demo: Populate Docker Volumes with Containers"
LABEL org.opencontainers.image.description="A Dockerfile demo illustrating how to populate Docker volumes using containers and serving static content with NGINX."
LABEL org.opencontainers.image.version="1.0"

# Using COPY to copy a local file
COPY ./static-content/ /usr/share/nginx/html

