#!/bin/bash

echo ""
echo "========================================"
echo "   School Review Manager - Flask App"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env file with your MySQL credentials!"
    echo ""
    read -p "Press any key to continue..."
fi

# Run the application
echo ""
echo "Starting Flask application..."
echo "Visit http://localhost:5000 in your browser"
echo ""
python app.py
