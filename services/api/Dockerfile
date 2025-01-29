# Use a base image with Python 3.12
FROM python:3.12-slim-bookworm AS base

# Set environment variables
ENV PYTHON_VERSION="3.12"
ENV PYTHON_PIP_VERSION="23.3.1"

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    python3-venv \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python${PYTHON_VERSION} -m ensurepip --upgrade && \
    python${PYTHON_VERSION} -m pip install --no-cache-dir "pip==${PYTHON_PIP_VERSION}"

# Set up the working directory
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry==1.7.1

# Copy only the poetry.lock and pyproject.toml files first to leverage caching
COPY poetry.lock pyproject.toml ./

# Check if poetry.lock exists. If not, create an empty one.
RUN if [ ! -f poetry.lock ]; then poetry init --no-interaction; poetry lock; fi

# Install project dependencies (including dev dependencies)
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Copy the rest of the application code
COPY . .

# Expose the port your FastAPI app will run on
EXPOSE 8080

# Command to run the FastAPI application with hot reload
CMD ["poetry", "run", "fastapi", "run", "src", "--host", "0.0.0.0", "--port", "8080", "--reload"]
