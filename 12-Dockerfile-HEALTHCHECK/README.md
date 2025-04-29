# Use nginx:alpine-slim as base Docker Image
FROM nginx:alpine-slim

# OCI Labels
LABEL org.opencontainers.image.authors="Kalyan Reddy Daida"
LABEL org.opencontainers.image.title="Demo: HEALTHCHECK Instruction in Docker"
LABEL org.opencontainers.image.description="A Dockerfile demo illustrating the use of the HEALTHCHECK instruction"
LABEL org.opencontainers.image.version="1.0"

# Install curl (needed for our Healthcheck command)
RUN apk --no-cache add curl

# Using COPY to copy a local file
COPY index.html /usr/share/nginx/html

# The HEALTHCHECK instruction tells Docker how to test a container to check that it's still working
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --start-interval=5s --retries=3 CMD curl -f http://localhost/ || exit 1