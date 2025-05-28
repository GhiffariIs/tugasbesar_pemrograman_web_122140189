@echo off
REM Script to run the Aturmation backend
REM This batch file helps with common development tasks

if "%1"=="" goto help
if "%1"=="install" goto install
if "%1"=="serve" goto serve
if "%1"=="init" goto init
if "%1"=="test" goto test
if "%1"=="cov" goto coverage
goto help

:install
echo Installing dependencies...
pip install -e .
pip install -e ".[testing]"
echo Dependencies installed.
goto end

:serve
echo Starting the server...
python main.py
goto end

:init
echo Initializing database...
python -m aturmation.scripts.initialize_db development.ini
echo Database initialized.
goto end

:test
echo Running tests...
pytest -v
goto end

:coverage
echo Generating test coverage report...
pytest --cov=aturmation --cov-report=term-missing
goto end

:help
echo.
echo Aturmation Backend Management Script
echo ------------------------------------
echo Usage: run.bat [command]
echo.
echo Available commands:
echo   install  - Install dependencies
echo   serve    - Start the server
echo   init     - Initialize database
echo   test     - Run tests
echo   cov      - Generate test coverage report
echo.

:end
