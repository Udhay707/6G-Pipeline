#!/bin/bash

# Get the directory of the current script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Navigate to the project root directory
cd "$SCRIPT_DIR/../.."

# Print the current working directory to verify
echo "Current directory: $(pwd)"

# Shut down the existing stack
echo "Shutting down the existing stack..."
docker compose -f docker-compose-core.yaml down --remove-orphans

# Start the 5G core
echo "Starting the 5G core..."
docker compose -f docker-compose-core.yaml up -d

# Wait for 15 seconds
echo "Waiting for 15 seconds..."
sleep 15

echo "Done!"