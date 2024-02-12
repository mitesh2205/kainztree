# Kainztree Django Rest Framework Project

Brief description of your project.

## Getting Started

These instructions will help you set up and run the project on your local machine.

### Prerequisites

Make sure you have the following installed:

- Python (version >= 3.6)
- pip (Python package installer)

### Installing Dependencies

```bash
pip install -r requirements.txt
```

### Setting up the Database
    
```bash
python manage.py migrate
python manage.py migrate inventory
```

### Running the Server

```bash
python manage.py runserver
```

### Running the Tests

```bash
python manage.py test inventory.test
```

## API Documentation

The API documentation is available at [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)

### Used Technologies

- Django
- Django Rest Framework
- PostgreSQL
- Swagger