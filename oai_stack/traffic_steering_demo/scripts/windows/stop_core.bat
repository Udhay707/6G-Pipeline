@echo off

:: Get the directory of the current script
set SCRIPT_DIR=%~dp0

:: Navigate to the project root directory (two levels up from the script's directory)
cd /d "%SCRIPT_DIR%..\.."

:: Print the current working directory to verify
echo Current directory: %cd%

:: Shut down the existing stack
echo Shutting down the existing stack...
docker compose -f docker-compose-core.yaml down --remove-orphans

echo Done!