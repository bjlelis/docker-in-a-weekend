# Use the official Python image as the base image
# This image comes with Python pre-installed
FROM python

# Set the working directory inside the container to /usr/src/app
# All subsequent commands will be run from this directory
WORKDIR /usr/src/app

# Copy the contents of the current directory on the host (where the Dockerfile is located) to /usr/src/app in the container
# using pattern matching COPY command
COPY *.py .

# Install the Flask package using pip
# The --no-cache-dir option ensures no cache is used, reducing the image size
RUN pip install --no-cache-dir flask

# Explicitly set the USER environment variable for the non-root user
ENV USER=mypythonuser
ENV GROUP=mypythongroup

# Create a new group called 'mygroup' and a non-root user 'mypythonuser' within this group
# -m creates a home directory for the user
RUN groupadd -r ${GROUP} && useradd -m -r -g ${GROUP} ${USER}

# Set ownership of the /usr/src/app directory to the non-root user 'mypythonuser'
# This ensures that 'mypythonuser' has the necessary permissions to access the app directory
RUN chown -R ${USER}:${GROUP} /usr/src/app

# Switch to the non-root user 'mypythonuser' so that the application does not run as root
USER ${USER}

# Command to run the Python application
# This command starts the Flask app when the container starts
CMD ["python", "app.py"]

# Expose port 5000 to the host, so the Flask app is accessible externally
EXPOSE 5000
