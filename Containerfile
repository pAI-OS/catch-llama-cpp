# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies required for potential binary handling and other operations
RUN apt-get update && apt-get install -y --no-install-recommends \
    zip \
    unzip \
    tar \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Run latest-llama-cpp.py when the container launches
CMD ["python", "latest-llama-cpp.py"]
