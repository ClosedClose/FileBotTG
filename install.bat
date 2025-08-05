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

echo Downloading latest yt-dlp.exe...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe' -OutFile 'yt-dlp.exe'"
if %ERRORLEVEL% neq 0 (
    echo Failed to download yt-dlp.exe.
    exit /b %ERRORLEVEL%
)

echo Downloading latest ffmpeg release...
powershell -Command "Invoke-WebRequest -Uri 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip' -OutFile 'ffmpeg.zip'"
if %ERRORLEVEL% neq 0 (
    echo Failed to download ffmpeg release.
    exit /b %ERRORLEVEL%
)

echo Extracting ffmpeg binaries...
powershell -Command "Expand-Archive -Path 'ffmpeg.zip' -DestinationPath 'ffmpeg-temp' -Force"
if %ERRORLEVEL% neq 0 (
    echo Failed to extract ffmpeg release.
    exit /b %ERRORLEVEL%
)

for /d %%i in (ffmpeg-temp\*) do (
    if exist "%%i\bin\ffmpeg.exe" (
        copy /Y "%%i\bin\ffmpeg.exe" .
        copy /Y "%%i\bin\ffplay.exe" .
        copy /Y "%%i\bin\ffprobe.exe" .
    )
)
if %ERRORLEVEL% neq 0 (
    echo Failed to copy ffmpeg binaries.
    exit /b %ERRORLEVEL%
)

rd /s /q ffmpeg-temp
del ffmpeg.zip

echo All downloads completed successfully!

echo Setup completed successfully!