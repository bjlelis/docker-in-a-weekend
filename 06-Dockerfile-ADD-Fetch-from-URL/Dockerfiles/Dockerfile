# Use nginx:alpine-slim as base Docker Image
FROM nginx:alpine-slim

# OCI Labels
LABEL org.opencontainers.image.authors="Kalyan Reddy Daida"
LABEL org.opencontainers.image.title="Demo: Using ADD Instruction to Fetch Files from a URL in Dockerfile"
LABEL org.opencontainers.image.description="A Dockerfile demo illustrating the ADD instruction, which demonstrates how to download and add content from a GitHub Releases URL to the container."
LABEL org.opencontainers.image.version="1.0"

# Using GitHub Repository to download files
ADD https://github.com/stacksimplify/docker-add-fetch-url-demo.git#v1.0.0:docs /usr/share/nginx/html
