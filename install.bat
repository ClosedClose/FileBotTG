@echo off
echo Creating Python virtual environment...
python -m venv venv
if %ERRORLEVEL% neq 0 (
    echo Failed to create virtual environment.
    exit /b %ERRORLEVEL%
)

echo Activating virtual environment...
call venv\Scripts\activate.bat
if %ERRORLEVEL% neq 0 (
    echo Failed to activate virtual environment.
    exit /b %ERRORLEVEL%
)

echo Installing dependencies from requirements.txt...
pip install -r req.txt
if %ERRORLEVEL% neq 0 (
    echo Failed to install dependencies.
    exit /b %ERRORLEVEL%
)

echo Setup completed successfully!