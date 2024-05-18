#!/bin/bash
# chmod +x scripts/install_packages.sh
# ./scripts/install_packages.sh

# Check if the .env file exists. If not, throw an error.
if [ ! -f .env ]; then
    echo "Error: .env file not found! Please create a .env file and fill it with valid environment variables for the project."
    exit 1
fi

# Check if the venv folder does not exist
if [ ! -d "venv" ]; then
    echo "venv folder not found. Creating a venv folder."

    echo "Executing command: python3 -m pip install virtualenv"
    # Install the virtualenv package
    python3 -m pip install virtualenv

    echo "Executing command: python3 -m virtualenv venv"
    # Create a virtual environment with Python 3.9
    python3 -m virtualenv venv

else
    echo "venv folder found."
fi

echo "Executing command: source venv/bin/activate"
# Activate virtual environment based on the operating system
if [ "$(uname)" == "Darwin" ] || [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    echo "Detected Unix-based system"
    source venv/bin/activate
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ] || [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
    echo "Detected Windows system"
    source venv/Scripts/activate
else
    echo "Unsupported operating system"
    exit 1
fi
echo "Executing command: pip install --upgrade pip"
# Upgrade pip
pip install --upgrade pip

echo "Executing command: pip install -r requirements.txt"
# Install the necessary packages for the project
pip install -r requirements.txt
