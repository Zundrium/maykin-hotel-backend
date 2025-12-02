#!/bin/bash

# Maykin CSV Model Sync - Setup Script
# This script sets up and runs the project according to the README

set -e  # Exit on error

echo "=== Maykin CSV Model Sync Setup ==="
echo ""

# Step 1: Create virtual environment
echo "Step 1: Creating virtual environment..."
python3 -m venv .venv
echo "✓ Virtual environment created"
echo ""

# Step 2: Install dependencies
echo "Step 2: Installing dependencies..."
.venv/bin/pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Step 3: Setup environment file
echo "Step 3: Setting up environment file..."
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✓ Created .env from .env.example"
    else
        echo "⚠ Warning: .env.example not found!"
        echo "Please create a .env file manually"
        exit 1
    fi
else
    echo "✓ .env file already exists"
fi
echo ""

# Step 4: Apply migrations
echo "Step 4: Applying database migrations..."
.venv/bin/python manage.py migrate
echo "✓ Migrations applied"
echo ""

# Step 5: Import hotel data
echo "Step 5: Importing hotel data..."
.venv/bin/python manage.py import_hotel_data
echo "✓ Hotel data imported"
echo ""

# Step 6: Run server
echo "=== Setup Complete ==="
echo ""
echo "To start the development server, run:"
echo "  source .venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Or run it directly with:"
echo "  .venv/bin/python manage.py runserver"
