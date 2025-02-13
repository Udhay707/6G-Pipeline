#!/bin/bash
ue="$1"

if [[ "$ue" != "gnbsim-vpp" && "$ue" != "gnbsim-vpp2" ]]; then
    echo "Invalid arguments"
    exit 1
fi

# Get the directory of the current script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Navigate to the project root directory
cd "$SCRIPT_DIR/../.."

# Print the current working directory to verify
echo "Current directory: $(pwd)"

echo "Stopping the RAN {$ue}"
docker compose -f docker-compose-ran-ue.yaml down "$ue"
sleep 1
docker compose -f docker-compose-ran-ue.yaml up "$ue" -d
echo "Restarted $ue successfully"