##### Stage 1: Builder Stage #####
FROM node:bookworm AS builder

# Set Working Directory
WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install --production

# Copy the application source code
COPY *.js .

##### Stage 2: Final Stage ##### 
FROM node:bookworm-slim AS final  

# Set Working Directory
WORKDIR /app

# Copy the necessary files from the builder stage
COPY --from=builder /app ./

# Expose the application port
EXPOSE 8080

# Start the application
CMD ["npm", "start"]
