# Use an official Python runtime as the base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the Python script into the container
COPY . .

# Run the script when the container launches
CMD ["python", "./main.py"]