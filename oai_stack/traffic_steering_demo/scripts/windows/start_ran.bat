@echo off

:: Get the directory of the current script
set SCRIPT_DIR=%~dp0

:: Navigate to the project root directory (two levels up from the script's directory)
cd /d "%SCRIPT_DIR%..\.."

:: Print the current working directory to verify
echo Current directory: %cd%

:: Start the first RAN/UE
echo Starting the first RAN/UE ...
docker compose -f docker-compose-ran-ue.yaml up gnbsim-vpp -d

:: Wait for 10 seconds
echo Waiting for 10 seconds...
timeout /t 10 /nobreak >nul

:: Start the Second RAN/UE
echo Starting the second RAN/UE ...
docker compose -f docker-compose-ran-ue.yaml up gnbsim-vpp2 -d

echo Done!