# Aturmation - Backend API

Backend service for Aturmation, a stock management system with CRUD functionality for products, categories, and transaction recording.

## Technology Stack

- **Python Pyramid** - Web framework
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** - Database
- **JWT** - Authentication
- **Pytest** - Testing

## Features

- RESTful API with complete CRUD operations
- JWT-based authentication and authorization
- PostgreSQL database with SQLAlchemy ORM
- Transaction-based inventory management
- 60%+ test coverage with unit and functional tests

## API Endpoints

### Authentication
- `POST /api/login` - Login and get JWT token
- `POST /api/register` - Register a new user
- `POST /api/logout` - Logout (client-side)
- `GET /api/user` - Get authenticated user info

### Products
- `GET /api/products` - Get all products
- `GET /api/products/{id}` - Get product details by ID
- `POST /api/products` - Add a new product
- `PUT /api/products/{id}` - Update product by ID
- `DELETE /api/products/{id}` - Delete product by ID

### Categories
- `GET /api/categories` - Get all categories
- `GET /api/categories/{id}` - Get category details by ID
- `POST /api/categories` - Add a new category
- `PUT /api/categories/{id}` - Update category by ID
- `DELETE /api/categories/{id}` - Delete category by ID

### Transactions
- `GET /api/transactions` - Get all transactions
- `GET /api/transactions/{id}` - Get transaction details by ID
- `POST /api/transactions` - Add a new transaction

## Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL

### Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Create a PostgreSQL database:
```sql
CREATE DATABASE aturmation_db;
```

3. Install dependencies:
```bash
pip install -e .
```

4. Edit development.ini to set your PostgreSQL connection:
```ini
sqlalchemy.url = postgresql://username:password@localhost:5432/aturmation_db
```

5. Initialize database:
```bash
initialize_db development.ini
```

6. Run the application:
```bash
python main.py
```

The API will be available at http://localhost:6543

### Using Make (optional)

If you have Make installed, you can use the following commands:

```bash
make install    # Install dependencies
make develop    # Install in development mode
make initdb     # Initialize database
make serve      # Run the application
make test       # Run tests
make coverage   # Generate coverage report
```

## Testing

Run the test suite:
```bash
pytest -v
```

Generate coverage report:
```bash
pytest --cov=aturmation --cov-report=term-missing
```

Our test suite includes:
- Unit tests for models
- Unit tests for views
- Functional API tests

## API Authentication

The API uses JWT for authentication. To use protected endpoints:

1. First log in via `/api/login` to get a token
2. Include the token in the Authorization header: `Authorization: Bearer <token>`

## Database Schema

- **Users** - Authentication and authorization
- **Categories** - Product categorization
- **Products** - Inventory items with stock management
- **Transactions** - Record of inventory in/out events