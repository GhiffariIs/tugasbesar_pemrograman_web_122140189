#!/bin/bash
# Script to run the Aturmation backend
# This shell script helps with common development tasks

function show_help {
    echo
    echo "Aturmation Backend Management Script"
    echo "------------------------------------"
    echo "Usage: ./run.sh [command]"
    echo
    echo "Available commands:"
    echo "  install  - Install dependencies"
    echo "  serve    - Start the server"
    echo "  init     - Initialize database"
    echo "  test     - Run tests"
    echo "  cov      - Generate test coverage report"
    echo
}

case "$1" in
    install)
        echo "Installing dependencies..."
        pip install -e .
        pip install -e ".[testing]"
        echo "Dependencies installed."
        ;;
    serve)
        echo "Starting the server..."
        python main.py
        ;;
    init)
        echo "Initializing database..."
        python -m aturmation.scripts.initialize_db development.ini
        echo "Database initialized."
        ;;
    test)
        echo "Running tests..."
        pytest -v
        ;;
    cov)
        echo "Generating test coverage report..."
        pytest --cov=aturmation --cov-report=term-missing
        ;;
    *)
        show_help
        ;;
esac
