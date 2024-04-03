# Step 1: Base image
FROM node:16 AS build

# Step 2: Set working directory
WORKDIR /app

# Step 3: Copy project files to the container
COPY . .

# Step 4: Install dependencies
RUN npm install
# Set environment variable for VITE_SOCKET_URL
ARG FLASK_PORT
ENV VITE_SOCKET_URL=http://localhost:${FLASK_PORT}

# Step 5: Build the application for production
RUN npm run build

# Use a lighter node image to serve the build
FROM node:16-slim

# Install 'serve' to serve the app on container startup
RUN npm install -g serve

# Copy the build from the previous stage
COPY --from=build /app/dist /app

# Expose the port the app runs on
EXPOSE 5000

# Step 6: Run the application
CMD ["serve", "-s", "/app", "-l", "5000"]
