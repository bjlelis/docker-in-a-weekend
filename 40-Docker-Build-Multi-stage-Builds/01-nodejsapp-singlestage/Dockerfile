# Single-stage Dockerfile for Node.js app
FROM node:bookworm

# Set Working Directory
WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install --production

# Copy the application source code
COPY *.js .

# Expose the application port
EXPOSE 8080

# Start the application
CMD ["npm", "start"]
