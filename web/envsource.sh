#!/usr/bin/env bash

# Check if .env file exists
if [ ! -f .env ]; then
    echo ".env file not found"
    exit 1
fi

# Export each variable from the .env file
while IFS='=' read -r key value; do
    if [[ ! $key =~ ^# && $key =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]]; then
        export "$key=$value"
        echo "Exported: $key"
    fi
done <.env

echo "Environment variables from .env file have been exported."
