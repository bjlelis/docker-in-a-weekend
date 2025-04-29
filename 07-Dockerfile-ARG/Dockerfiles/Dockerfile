# Define a build-time argument for the NGINX version
ARG NGINX_VERSION=1.26

# Use nginx:alpine-slim as base Docker Image
FROM nginx:${NGINX_VERSION}-alpine-slim

# OCI Labels
LABEL org.opencontainers.image.authors="Kalyan Reddy Daida"
LABEL org.opencontainers.image.title="Demo: Using ARG Instruction"
LABEL org.opencontainers.image.description="A Dockerfile demo illustrating the ARG instruction"
LABEL org.opencontainers.image.version="1.0"

# Using COPY to copy a local file
COPY index.html /usr/share/nginx/html