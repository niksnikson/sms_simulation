# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5672 and 15672 available to the world outside this container
EXPOSE 5672 15672

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Define default command
CMD ["python", "producer.py"]
