#!/bin/bash
# Unix/Linux/macOS script to start the 3D Game Platform

echo "Starting 3D Game Platform..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ from your package manager or https://python.org"
    exit 1
fi

# Run the development server launcher
python3 run_dev.py