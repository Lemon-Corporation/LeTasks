# Use official Node.js image
FROM node:18-slim

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json /app/

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . /app

# Build the Vue.js app
RUN npm run build

# Install a simple HTTP server to serve the app
RUN npm install -g serve

# Expose the port for the frontend
EXPOSE 8080

# Command to run the server
CMD ["serve", "-s", "dist", "-l", "8080"]
