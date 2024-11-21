# Use an official Python runtime as the base image
FROM python:3.12

# Set the working directory in the container
WORKDIR /opt/project

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=.

# Install system dependencies and Python tools
RUN set -xe \
    && apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && pip install virtualenvwrapper poetry==1.8.4 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies files and install dependencies
COPY ["poetry.lock", "pyproject.toml", "./"]
RUN poetry install --no-root

# Copy project files
COPY ["README.md", "Makefile", "./"]
COPY core core

# Expose port 8000
EXPOSE 8000

# Copy and set up the entrypoint script
COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh

# Define the entrypoint
ENTRYPOINT ["/entrypoint.sh"]
