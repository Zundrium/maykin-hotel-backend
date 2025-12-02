@echo off
setlocal enabledelayedexpansion

REM Maykin CSV Model Sync - Setup Script
REM This script sets up and runs the project according to the README

echo === Maykin CSV Model Sync Setup ===
echo.

REM Step 1: Create virtual environment
echo Step 1: Creating virtual environment...
python -m venv .venv
if errorlevel 1 (
    echo ✗ Failed to create virtual environment
    exit /b 1
)
echo ✓ Virtual environment created
echo.

REM Step 2: Install dependencies
echo Step 2: Installing dependencies...
.venv\Scripts\pip install -r requirements.txt
if errorlevel 1 (
    echo ✗ Failed to install dependencies
    exit /b 1
)
echo ✓ Dependencies installed
echo.

REM Step 3: Setup environment file
echo Step 3: Setting up environment file...
if not exist .env (
    if exist .env.example (
        copy .env.example .env >nul
        echo ✓ Created .env from .env.example
    ) else (
        echo ⚠ Warning: .env.example not found!
        echo Please create a .env file manually
        exit /b 1
    )
) else (
    echo ✓ .env file already exists
)
echo.

REM Step 4: Apply migrations
echo Step 4: Applying database migrations...
.venv\Scripts\python manage.py migrate
if errorlevel 1 (
    echo ✗ Failed to apply migrations
    exit /b 1
)
echo ✓ Migrations applied
echo.

REM Step 5: Import hotel data
echo Step 5: Importing hotel data...
.venv\Scripts\python manage.py import_hotel_data
if errorlevel 1 (
    echo ✗ Failed to import hotel data
    exit /b 1
)
echo ✓ Hotel data imported
echo.

REM Step 6: Create test users
echo Step 6: Creating test users...
.venv\Scripts\python manage.py create_test_users
if errorlevel 1 (
    echo ✗ Failed to create test users
    exit /b 1
)
echo ✓ Test users created
echo.

REM Step 7: Run server
echo === Setup Complete ===
echo.
echo To start the development server, run:
echo   .venv\Scripts\activate
echo   python manage.py runserver
echo.
echo Or run it directly with:
echo   .venv\Scripts\python manage.py runserver

pause