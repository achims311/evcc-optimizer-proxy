#!/bin/bash

# Development script for local testing
# Usage: ./run-dev.sh

echo "Setting up development environment..."

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r rootfs/app/requirements.txt

# Set environment variables
export FLASK_APP=rootfs/app/main.py
export FLASK_ENV=development
export TARGET_URL=${TARGET_URL:-"https://optimizer.evcc.io"}
export LOG_LEVEL=${LOG_LEVEL:-"DEBUG"}
export USE_SYSTEM_PROXY=${USE_SYSTEM_PROXY:-"true"}

echo ""
echo "Development environment ready!"
echo ""
echo "Environment variables:"
echo "  TARGET_URL=$TARGET_URL"
echo "  LOG_LEVEL=$LOG_LEVEL"
echo "  USE_SYSTEM_PROXY=$USE_SYSTEM_PROXY"
echo ""
echo "Starting development server on http://localhost:8080"
echo ""

# Run the application
cd rootfs/app
python main.py
