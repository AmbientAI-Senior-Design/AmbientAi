# Step 1: Use the official Python image as the base image
FROM python:3.9

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the current directory contents into the container at /app
COPY . /app

# Step 4: Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Eventlet is recommended for the best performance with Flask-SocketIO
RUN pip install eventlet gunicorn

# Step 5: Make port 6942 available to the world outside this container
EXPOSE 6942

# Step 6: Define environment variable for Gunicorn to use eventlet workers
ENV WORKERS=4

# Step 7: Run the application using Gunicorn with eventlet worker class
CMD ["gunicorn", "-k", "eventlet", "-w", "1", "-b", "0.0.0.0:6942", "application:application"]
