# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install python-dotenv to load environment variables from .env file
RUN pip install --no-cache-dir python-dotenv

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir discord openai==0.28 requests

# Copy .env file into the container at /usr/src/app
COPY .env .env

# Run main.py when the container launches
CMD ["python", "main.py"]