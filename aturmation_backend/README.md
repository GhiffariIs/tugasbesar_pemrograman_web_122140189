# Aturmation Backend

A Python Pyramid RESTful API backend for the Aturmation Inventory Management System.

## Features

- RESTful API with CRUD operations
- JWT Authentication
- User Management
- Category Management
- Product Management
- Transaction Management
- Reporting

## Installation

```bash
# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Unix/MacOS

# Install the project in development mode
pip install -e .

# Initialize the database
initialize_db development.ini
```

## Running the Project

```bash
# For Windows
run.bat

# For Unix/MacOS
sh run.sh
```

## Testing

```bash
pytest
```

## API Documentation

API endpoints are available at http://localhost:6543/api
