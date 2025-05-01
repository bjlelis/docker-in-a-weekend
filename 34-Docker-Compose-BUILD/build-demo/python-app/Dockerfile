# Use the official Python image from the Docker Hub
FROM python:slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install the dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose the app on port 5000
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
