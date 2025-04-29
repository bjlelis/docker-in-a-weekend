# Use nginx:alpine-slim as base Docker Image
FROM nginx:alpine-slim

# OCI Labels
LABEL org.opencontainers.image.authors="Kalyan Reddy Daida"
LABEL org.opencontainers.image.title="Demo: Using RUN, EXPOSE Instructions in Dockerfile"
LABEL org.opencontainers.image.description="A Dockerfile demo illustrating the usage of RUN and EXPOSE instructions"
LABEL org.opencontainers.image.version="1.0"

# Copy all Nginx configuration files from nginx-conf directory
COPY nginx-conf/*.conf /etc/nginx/conf.d/

# Copy all HTML files from nginx-html directory
COPY nginx-html/*.html /usr/share/nginx/html/

# Install curl using RUN
RUN apk --no-cache add curl

# Expose the ports 8081, 8082, 8083 (default port 80 already exposed from base nginx image)
EXPOSE 8081 8082 8083
