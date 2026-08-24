FROM ubuntu:24.04

# Install system packages as root
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Create application user
RUN useradd -m apollo

# Run everything below as apollo
USER apollo

# Set the application working directory
WORKDIR /home/apollo/app