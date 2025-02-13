#!/bin/bash

# Get the directory of the current script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Navigate to the project root directory
cd "$SCRIPT_DIR/../.."

# Print the current working directory to verify
echo "Current directory: $(pwd)"

# Start the RAN
echo "Starting the RAN-1 (UE + gNB)"
docker compose -f docker-compose-ran-ue.yaml up gnbsim-vpp -d
echo "Sleeping for 10 seconds"
sleep 10

echo "Starting the RAN-2 (UE + gNB)"
docker compose -f docker-compose-ran-ue.yaml up gnbsim-vpp2 -d

echo "Done!"