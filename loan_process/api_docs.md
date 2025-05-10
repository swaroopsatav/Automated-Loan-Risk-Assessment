# Loan Processing System API Documentation

This document provides detailed information about the API endpoints available in the Loan Processing System.

## Authentication

The API uses JWT (JSON Web Token) authentication. To access protected endpoints, you need to include the JWT token in the Authorization header:

```
Authorization: Bearer <your_token>
```

### Getting a Token

To get a token, send a POST request to `/api/token/` with your username and password:

```http
POST /api/token/
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

Response:

```json
{
  "refresh": "your_refresh_token",
  "access": "your_access_token"
}
```

### Refreshing a Token

To refresh an expired token, send a POST request to `/api/token/refresh/` with your refresh token:

```http
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "your_refresh_token"
}
```

Response:

```json
{
  "access": "your_new_access_token"
}
```

## User Management API

### Register a New User

```http
POST /api/users/auth/register/
Content-Type: application/json

{
  "username": "newuser",
  "email": "user@example.com",
  "password": "securepassword",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+1234567890"
}
```

Response:

```json
{
  "id": 1,
  "username": "newuser",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+1234567890"
}
```

### User Login

```http
POST /api/users/auth/login/
Content-Type: application/json

{
  "username": "newuser",
  "password": "securepassword"
}
```

Response:

```json
{
  "token": "your_access_token",
  "user": {
    "id": 1,
    "username": "newuser",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

### Get User Profile

```http
GET /api/users/me/
Authorization: Bearer your_access_token
```

Response:

```json
{
  "id": 1,
  "username": "newuser",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+1234567890",
  "date_joined": "2023-01-01T12:00:00Z"
}
```

### Update User Profile

```http
PATCH /api/users/me/
Authorization: Bearer your_access_token
Content-Type: application/json

{
  "first_name": "Johnny",
  "phone_number": "+9876543210"
}
```

Response:

```json
{
  "id": 1,
  "username": "newuser",
  "email": "user@example.com",
  "first_name": "Johnny",
  "last_name": "Doe",
  "phone_number": "+9876543210",
  "date_joined": "2023-01-01T12:00:00Z"
}
```

### List All Users (Admin Only)

```http
GET /api/users/admin/users/
Authorization: Bearer your_access_token
```

Response:

```json
[
  {
    "id": 1,
    "username": "newuser",
    "email": "user@example.com",
    "first_name": "Johnny",
    "last_name": "Doe",
    "is_active": true,
    "date_joined": "2023-01-01T12:00:00Z"
  },
  {
    "id": 2,
    "username": "anotheruser",
    "email": "another@example.com",
    "first_name": "Jane",
    "last_name": "Smith",
    "is_active": true,
    "date_joined": "2023-01-02T12:00:00Z"
  }
]
```

### Get User Details (Admin Only)

```http
GET /api/users/admin/users/1/
Authorization: Bearer your_access_token
```

Response:

```json
{
  "id": 1,
  "username": "newuser",
  "email": "user@example.com",
  "first_name": "Johnny",
  "last_name": "Doe",
  "phone_number": "+9876543210",
  "is_active": true,
  "is_staff": false,
  "date_joined": "2023-01-01T12:00:00Z",
  "last_login": "2023-01-03T12:00:00Z"
}
```

## Loan Application API

### Submit a Loan Application

```http
POST /api/loans/submission/
Authorization: Bearer your_access_token
Content-Type: application/json

{
  "loan_amount": 10000,
  "loan_purpose": "Home Renovation",
  "loan_term_months": 24,
  "employment_status": "EMPLOYED",
  "annual_income": 75000,
  "address": "123 Main St, Anytown, USA",
  "existing_loans": 1,
  "credit_consent": true
}
```

Response:

```json
{
  "id": 1,
  "loan_amount": 10000,
  "loan_purpose": "Home Renovation",
  "loan_term_months": 24,
  "employment_status": "EMPLOYED",
  "annual_income": 75000,
  "address": "123 Main St, Anytown, USA",
  "existing_loans": 1,
  "status": "PENDING",
  "created_at": "2023-01-04T12:00:00Z",
  "updated_at": "2023-01-04T12:00:00Z",
  "user": 1
}
```

### List User's Loan Applications

```http
GET /api/loans/
Authorization: Bearer your_access_token
```

Response:

```json
[
  {
    "id": 1,
    "loan_amount": 10000,
    "loan_purpose": "Home Renovation",
    "status": "PENDING",
    "created_at": "2023-01-04T12:00:00Z"
  },
  {
    "id": 2,
    "loan_amount": 5000,
    "loan_purpose": "Education",
    "status": "APPROVED",
    "created_at": "2023-01-05T12:00:00Z"
  }
]
```

### Get Loan Application Details

```http
GET /api/loans/1/
Authorization: Bearer your_access_token
```

Response:

```json
{
  "id": 1,
  "loan_amount": 10000,
  "loan_purpose": "Home Renovation",
  "loan_term_months": 24,
  "employment_status": "EMPLOYED",
  "annual_income": 75000,
  "address": "123 Main St, Anytown, USA",
  "existing_loans": 1,
  "status": "PENDING",
  "created_at": "2023-01-04T12:00:00Z",
  "updated_at": "2023-01-04T12:00:00Z",
  "documents": [],
  "credit_score": null
}
```

### Upload Loan Document

```http
POST /api/loans/1/documents/
Authorization: Bearer your_access_token
Content-Type: multipart/form-data

{
  "document_type": "INCOME_PROOF",
  "file": <file_upload>
}
```

Response:

```json
{
  "id": 1,
  "document_type": "INCOME_PROOF",
  "file": "/media/loan_documents/1/income_proof.pdf",
  "uploaded_at": "2023-01-04T13:00:00Z",
  "loan": 1
}
```

### List All Loan Applications (Admin Only)

```http
GET /api/loans/admin/
Authorization: Bearer your_access_token
```

Response:

```json
[
  {
    "id": 1,
    "user": {
      "id": 1,
      "username": "newuser",
      "email": "user@example.com"
    },
    "loan_amount": 10000,
    "loan_purpose": "Home Renovation",
    "status": "PENDING",
    "created_at": "2023-01-04T12:00:00Z"
  },
  {
    "id": 2,
    "user": {
      "id": 2,
      "username": "anotheruser",
      "email": "another@example.com"
    },
    "loan_amount": 5000,
    "loan_purpose": "Education",
    "status": "APPROVED",
    "created_at": "2023-01-05T12:00:00Z"
  }
]
```

### Get Loan Application Details (Admin Only)

```http
GET /api/loans/admin/1/
Authorization: Bearer your_access_token
```

Response:

```json
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "newuser",
    "email": "user@example.com",
    "first_name": "Johnny",
    "last_name": "Doe"
  },
  "loan_amount": 10000,
  "loan_purpose": "Home Renovation",
  "loan_term_months": 24,
  "employment_status": "EMPLOYED",
  "annual_income": 75000,
  "address": "123 Main St, Anytown, USA",
  "existing_loans": 1,
  "status": "PENDING",
  "created_at": "2023-01-04T12:00:00Z",
  "updated_at": "2023-01-04T12:00:00Z",
  "documents": [
    {
      "id": 1,
      "document_type": "INCOME_PROOF",
      "file": "/media/loan_documents/1/income_proof.pdf",
      "uploaded_at": "2023-01-04T13:00:00Z"
    }
  ],
  "credit_score": null,
  "compliance_checks": []
}
```

### Update Loan Application Status (Admin Only)

```http
PATCH /api/loans/admin/1/
Authorization: Bearer your_access_token
Content-Type: application/json

{
  "status": "APPROVED"
}
```

Response:

```json
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "newuser",
    "email": "user@example.com"
  },
  "loan_amount": 10000,
  "loan_purpose": "Home Renovation",
  "status": "APPROVED",
  "updated_at": "2023-01-04T14:00:00Z"
}
```

## Credit Scoring API

### Get Credit Score for a Loan

```http
GET /api/credit/loans/1/score/
Authorization: Bearer your_access_token
```

Response:

```json
{
  "id": 1,
  "score": 720,
  "risk_category": "LOW",
  "calculated_at": "2023-01-04T12:05:00Z",
  "loan": 1
}
```

### List All Credit Scores (Admin Only)

```http
GET /api/credit/admin/scores/
Authorization: Bearer your_access_token
```

Response:

```json
[
  {
    "id": 1,
    "score": 720,
    "risk_category": "LOW",
    "calculated_at": "2023-01-04T12:05:00Z",
    "loan": 1
  },
  {
    "id": 2,
    "score": 650,
    "risk_category": "MEDIUM",
    "calculated_at": "2023-01-05T12:05:00Z",
    "loan": 2
  }
]
```

### Get Credit Score Details (Admin Only)

```http
GET /api/credit/admin/scores/1/
Authorization: Bearer your_access_token
```

Response:

```json
{
  "id": 1,
  "score": 720,
  "risk_category": "LOW",
  "calculated_at": "2023-01-04T12:05:00Z",
  "factors": {
    "income_factor": 0.8,
    "employment_factor": 0.9,
    "existing_loans_factor": 0.7,
    "loan_amount_factor": 0.85
  },
  "loan": {
    "id": 1,
    "user": {
      "id": 1,
      "username": "newuser"
    },
    "loan_amount": 10000,
    "status": "PENDING"
  }
}
```

### Re-score a Loan Application (Admin Only)

```http
POST /api/credit/admin/loans/1/rescore/
Authorization: Bearer your_access_token
```

Response:

```json
{
  "id": 3,
  "score": 725,
  "risk_category": "LOW",
  "calculated_at": "2023-01-04T15:00:00Z",
  "loan": 1,
  "previous_score": 720
}
```

## Compliance API

### Get Compliance Checks for a Loan (Admin Only)

```http
GET /api/compliance/loans/1/checks/
Authorization: Bearer your_access_token
```

Response:

```json
[
  {
    "id": 1,
    "check_type": "IDENTITY_VERIFICATION",
    "status": "PASSED",
    "created_at": "2023-01-04T12:10:00Z",
    "updated_at": "2023-01-04T12:10:00Z",
    "loan": 1
  },
  {
    "id": 2,
    "check_type": "ANTI_MONEY_LAUNDERING",
    "status": "PENDING",
    "created_at": "2023-01-04T12:10:00Z",
    "updated_at": "2023-01-04T12:10:00Z",
    "loan": 1
  }
]
```

### Update Compliance Check Status (Admin Only)

```http
PATCH /api/compliance/checks/2/
Authorization: Bearer your_access_token
Content-Type: application/json

{
  "status": "PASSED",
  "notes": "All documents verified"
}
```

Response:

```json
{
  "id": 2,
  "check_type": "ANTI_MONEY_LAUNDERING",
  "status": "PASSED",
  "notes": "All documents verified",
  "created_at": "2023-01-04T12:10:00Z",
  "updated_at": "2023-01-04T15:30:00Z",
  "loan": 1
}
```

### Get Compliance Audit Trail (Admin Only)

```http
GET /api/compliance/audit-trail/
Authorization: Bearer your_access_token
```

Response:

```json
[
  {
    "id": 1,
    "action": "UPDATE",
    "entity_type": "COMPLIANCE_CHECK",
    "entity_id": 2,
    "previous_state": {
      "status": "PENDING",
      "notes": null
    },
    "new_state": {
      "status": "PASSED",
      "notes": "All documents verified"
    },
    "performed_by": {
      "id": 1,
      "username": "admin"
    },
    "timestamp": "2023-01-04T15:30:00Z"
  }
]
```

## Risk Dashboard API

### Get Risk Overview (Admin Only)

```http
GET /api/risk/overview/
Authorization: Bearer your_access_token
```

Response:

```json
{
  "total_loans": 100,
  "risk_distribution": {
    "HIGH": 15,
    "MEDIUM": 35,
    "LOW": 50
  },
  "average_score": 685,
  "approval_rate": 0.75,
  "rejection_rate": 0.25
}
```

### Get Risk Metrics by Time Period (Admin Only)

```http
GET /api/risk/metrics/?period=monthly
Authorization: Bearer your_access_token
```

Response:

```json
[
  {
    "period": "2023-01",
    "total_loans": 30,
    "average_score": 680,
    "approval_rate": 0.73,
    "risk_distribution": {
      "HIGH": 5,
      "MEDIUM": 10,
      "LOW": 15
    }
  },
  {
    "period": "2023-02",
    "total_loans": 35,
    "average_score": 690,
    "approval_rate": 0.77,
    "risk_distribution": {
      "HIGH": 4,
      "MEDIUM": 12,
      "LOW": 19
    }
  }
]
```

## Integrations API

### Verify External Credit Report

```http
POST /api/integrations/credit-verification/
Authorization: Bearer your_access_token
Content-Type: application/json

{
  "loan_id": 1,
  "provider": "EXPERIAN"
}
```

Response:

```json
{
  "id": 1,
  "status": "INITIATED",
  "provider": "EXPERIAN",
  "reference_id": "EXP-12345",
  "created_at": "2023-01-04T16:00:00Z",
  "loan": 1
}
```

### Get External Verification Status

```http
GET /api/integrations/credit-verification/1/
Authorization: Bearer your_access_token
```

Response:

```json
{
  "id": 1,
  "status": "COMPLETED",
  "provider": "EXPERIAN",
  "reference_id": "EXP-12345",
  "result": {
    "score": 715,
    "report_date": "2023-01-04",
    "matches_internal": true
  },
  "created_at": "2023-01-04T16:00:00Z",
  "updated_at": "2023-01-04T16:05:00Z",
  "loan": 1
}
```

## Error Responses

The API returns standard HTTP status codes to indicate the success or failure of a request:

- 200 OK: The request was successful
- 201 Created: A new resource was created successfully
- 400 Bad Request: The request was invalid or cannot be served
- 401 Unauthorized: Authentication is required or has failed
- 403 Forbidden: The authenticated user does not have permission to access the resource
- 404 Not Found: The requested resource does not exist
- 500 Internal Server Error: An error occurred on the server

Error response format:

```json
{
  "detail": "Error message"
}
```

For validation errors:

```json
{
  "field_name": [
    "Error message"
  ]
}
```

## Rate Limiting

The API implements rate limiting to prevent abuse. The current limits are:

- Anonymous users: 20 requests per minute
- Authenticated users: 100 requests per minute
- Authentication endpoints: 5 requests per minute

When a rate limit is exceeded, the API returns a 429 Too Many Requests response with a Retry-After header indicating how long to wait before making another request.