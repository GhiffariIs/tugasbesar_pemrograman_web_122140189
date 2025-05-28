# Aturmation Backend

Aturmation Backend is a RESTful API built using Python Pyramid. This project provides a robust backend solution for managing user data with CRUD operations and basic authentication.

## Project Structure

```
aturmation_backend
├── aturmation_backend
│   ├── __init__.py          # Initializes the Pyramid application
│   ├── models
│   │   ├── __init__.py      # Initializes the models package
│   │   └── user.py          # Defines the User model
│   ├── routes.py            # Defines the API routes
│   ├── security.py          # Implements basic authentication
│   ├── views
│   │   ├── __init__.py      # Initializes the views package
│   │   └── default.py       # Contains view functions for CRUD operations
│   └── templates            # Directory for HTML templates (if applicable)
├── tests
│   ├── __init__.py          # Initializes the tests package
│   └── test_views.py        # Contains unit tests for view functions
├── venv                      # Virtual environment directory
├── development.ini          # Configuration for development environment
├── production.ini           # Configuration for production environment
├── MANIFEST.in              # Specifies additional files for package distribution
├── README.md                # Documentation for the project
├── setup.py                 # Configuration for packaging the project
└── requirements.txt         # Lists required Python packages
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd aturmation_backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, use the following command:
```
pserve development.ini
```

## Testing

To run the unit tests and ensure at least 60% coverage, use:
```
pytest --cov=aturmation_backend tests/
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.