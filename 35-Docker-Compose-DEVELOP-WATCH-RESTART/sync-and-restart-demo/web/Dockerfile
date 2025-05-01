# Use the official NGINX base image
FROM nginx:latest

# Copy custom NGINX configuration file to replace the default.conf
COPY ./nginx.conf /etc/nginx/nginx.conf

# Copy static website files to the container's HTML directory
COPY ./html /usr/share/nginx/html

# Expose port 8080 for external access
EXPOSE 8080

# Start NGINX
CMD ["nginx", "-g", "daemon off;"]
