#!/bin/bash
# chmod +x scripts/run_docker.sh
# ./scripts/run_docker.sh

# Check if .env file already exists
if [ -e .env ]; then
    echo ".env file already exists."
else
    echo "No .env file found. Please create a new .env file."
    echo "You can use the .env.example file as a template and update it according to your needs."
    exit 1  # Exit with an error code
fi

# Run docker-compose with provided NAS credentials
docker-compose down --volumes --remove-orphans && \
# For debugging, add "--progress=plain" option to build command
docker-compose build --no-cache && \
docker-compose up -d --force-recreate
