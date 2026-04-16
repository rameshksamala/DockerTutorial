# Use official NGINX image
FROM nginx:alpine

# Copy custom HTML file to NGINX web root
COPY index.html /usr/share/nginx/html/index.html

# Expose port 80
EXPOSE 80

# Start NGINX
CMD ["nginx", "-g", "daemon off;"]
