@echo off
echo ========================================
echo   NexGenMusic Server Startup
echo ========================================
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if activation worked
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    echo Please make sure venv exists.
    pause
    exit /b 1
)

echo Virtual environment activated!
echo.

REM Show Python location
echo Using Python from:
where python
echo.

REM Check required packages
echo Checking required packages...
python -c "import soundfile; print('✓ soundfile:', soundfile.__version__)" 2>nul || echo ✗ soundfile NOT installed
python -c "import scipy; print('✓ scipy:', scipy.__version__)" 2>nul || echo ✗ scipy NOT installed
python -c "import django; print('✓ django:', django.__version__)" 2>nul || echo ✗ django NOT installed
echo.

REM Start server
echo Starting Django server...
echo Server will be available at: http://127.0.0.1:8000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python manage.py runserver

pause
