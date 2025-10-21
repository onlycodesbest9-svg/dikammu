#!/bin/bash

echo "========================================"
echo " RecursiveLearn Launcher"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.10 or higher"
    exit 1
fi

echo "Starting RecursiveLearn..."
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found."
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Could not create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
source venv/bin/activate

# Check if dependencies are installed
python -c "import PySide6" &> /dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Could not install dependencies"
        exit 1
    fi
fi

# Run the application
python main.py

# Deactivate virtual environment
deactivate

echo
echo "RecursiveLearn closed."
