# Use an official Python runtime as a parent image
FROM openjdk:8-jdk-slim

# Set the working directory in the container
WORKDIR /app

# Install Python and other dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Copy the entire src directory into the container
COPY ./src /app/src

# Set the entry point to run the main.py script
ENTRYPOINT ["python3", "src/main.py"]
