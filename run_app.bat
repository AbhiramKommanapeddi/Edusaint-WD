@echo off
echo.
echo ========================================
echo    School Review Manager - Flask App
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo.
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo ⚠️  IMPORTANT: Please edit .env file with your MySQL credentials!
    echo.
    pause
)

REM Run the application
echo.
echo Starting Flask application...
echo Visit http://localhost:5000 in your browser
echo.
python app.py

pause
