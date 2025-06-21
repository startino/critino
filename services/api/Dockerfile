FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Change the working directory to the `app` directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    python3-venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY uv.lock /app/uv.lock
COPY pyproject.toml /app/pyproject.toml

RUN uv sync --frozen --no-install-project

# Copy the project into the image
COPY . /app

# Sync the project into a new environment, using the frozen lockfile
RUN uv sync

# Command to run the FastAPI application with hot reload
CMD ["uv", "run", "fastapi", "run", "src", "--host", "0.0.0.0", "--port", "8080", "--reload"]
