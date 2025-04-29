# Use python:3.12-alpine as the base image
FROM python:3.12-alpine

# OCI Labels
LABEL org.opencontainers.image.authors="Kalyan Reddy Daida"
LABEL org.opencontainers.image.title="Demo: ARG vs ENV in Docker"
LABEL org.opencontainers.image.description="A Dockerfile demo illustrating the difference between ARG (build-time) and ENV (runtime) instructions"
LABEL org.opencontainers.image.version="1.0"

# Define build-time argument for environment (defaults to "dev")
ARG ENVIRONMENT=dev

# Set the ENV variable using the ARG value
ENV APP_ENVIRONMENT=${ENVIRONMENT}

# Set the working directory inside the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt requirements.txt

# Install packages from requirements.txt
RUN pip install -r requirements.txt

# Copy the application code
COPY app.py .

# Copy the templates directory
COPY templates/ ./templates/

# Print the environment for demo purposes
RUN echo "Building for environment: ${APP_ENVIRONMENT}"

# Start the Flask app
CMD ["python", "app.py"]
