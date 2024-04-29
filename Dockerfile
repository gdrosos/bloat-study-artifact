# Use Ubuntu 20.04 LTS as the base image
FROM  ubuntu:20.04
# Set the timezone environment variable
ENV TZ=Europe/Zurich

# Set the timezone and update the system packages
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    apt-get update -yqq && \
    apt-get upgrade -yqq && \
    apt-get install -yqq git python3-pip sudo wget unzip python3-venv

# Install Python packages from requirements.txt
# Ensure requirements.txt is in the same directory as the Dockerfile when building
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
RUN ln -s /usr/bin/python3 /usr/bin/python

# Create a non-root user
RUN useradd -ms /bin/bash user && \
    echo user:user | chpasswd && \
    cp /etc/sudoers /etc/sudoers.bak && \
    echo 'user ALL=(ALL:ALL) NOPASSWD:ALL' >> /etc/sudoers

# Switch to the user's home directory
USER user
WORKDIR /home/user

# Set up the working environment
COPY --chown=user:user requirements.txt ./
RUN pip3 install --user -r requirements.txt