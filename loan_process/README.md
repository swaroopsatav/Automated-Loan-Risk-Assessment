# Loan Processing System

## Overview

The Loan Processing System is a comprehensive Django-based web application designed to manage the entire loan application lifecycle. It provides a robust backend API and a React frontend for loan application submission, processing, approval, and management.

## Features

- User authentication and authorization
- Loan application submission and tracking
- Credit scoring and risk assessment
- Compliance checks and verification
- Document upload and management
- Risk dashboards and analytics
- Email notifications at various stages of the loan process
- Integration with external services

## Project Structure

The project is organized into several Django apps, each responsible for a specific aspect of the loan processing system:

- **users**: User management, authentication, and authorization
- **loanapplications**: Core loan application functionality
- **creditscorings**: Credit score calculation and management
- **compliances**: Regulatory compliance checks and verification
- **integrations**: Integration with external services and APIs
- **riskdashboards**: Risk assessment and analytics dashboards
- **frontend**: React-based user interface

## Technology Stack

### Backend
- Django 4.2+
- Django REST Framework
- MySQL Database
- JWT Authentication
- Asynchronous processing with Django ASGI

### Frontend
- React with Vite
- React Router
- Axios for API communication
- Responsive design with CSS frameworks

## Installation and Setup

### Prerequisites
- Python 3.10+
- Node.js 16+
- MySQL 8.0+
- Git

### Backend Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd loan_process
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database in `loan_process/settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'loan_approval',
           'USER': 'loan_user',
           'PASSWORD': 'your-password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

## API Documentation

The API endpoints are organized by module:

- `/api/users/` - User management endpoints
- `/api/loans/` - Loan application endpoints
- `/api/credit/` - Credit scoring endpoints
- `/api/integrations/` - External integration endpoints
- `/api/risk/` - Risk assessment endpoints
- `/api/compliance/` - Compliance check endpoints
- `/api/token/` - JWT token acquisition
- `/api/token/refresh/` - JWT token refresh

### Documentation Resources

- **Static Documentation**: See the [API Documentation](./api_docs.md) file for detailed endpoint descriptions, request/response formats, and examples.

- **Interactive Documentation**: Once the server is running, you can access the interactive API documentation at:
  - `/api/docs/` - Browse and test API endpoints through a web interface
  - `/api/schema/` - View the OpenAPI schema definition

The interactive documentation allows you to explore the API, see available endpoints, and even make test requests directly from your browser.

## Database Schema

The database schema for the Loan Processing System is documented in the [Database Schema](./database_schema.md) file. This documentation includes:

- Entity relationship diagram
- Detailed table descriptions
- Field definitions and types
- Table relationships
- Recommended indexes

## Configuration

### Email Configuration

Email settings are configured in `loan_process/settings.py`. For production, update the following settings:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.your-email-provider.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-email-password'
DEFAULT_FROM_EMAIL = 'Loan Processing System <your-email@example.com>'
```

### Security Configuration

For production deployment, ensure the following settings are properly configured:

```python
DEBUG = False
SECRET_KEY = 'your-secure-secret-key'
ALLOWED_HOSTS = ['your-domain.com']
CORS_ALLOWED_ORIGINS = ['https://your-frontend-domain.com']
```

## Testing

Run the test suite with:

```bash
python manage.py test
```

For email functionality testing:

```bash
python manage.py shell < test_email.py
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
