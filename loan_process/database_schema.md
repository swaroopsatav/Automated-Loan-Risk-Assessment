# Loan Processing System Database Schema

This document provides an overview of the database schema used in the Loan Processing System.

## Entity Relationship Diagram

```
+-------------------+       +----------------------+       +-------------------+
|    CustomUser     |       |   LoanApplication    |       |    CreditScore    |
+-------------------+       +----------------------+       +-------------------+
| id (PK)           |       | id (PK)              |       | id (PK)           |
| username          |       | user_id (FK)         |<----->| loan_id (FK)      |
| email             |<----->| loan_amount          |       | score             |
| first_name        |       | loan_purpose         |       | risk_category     |
| last_name         |       | loan_term_months     |       | calculated_at     |
| phone_number      |       | employment_status    |       | factors           |
| is_active         |       | annual_income        |       +-------------------+
| is_staff          |       | address              |
| date_joined       |       | existing_loans       |       +-------------------+
| last_login        |       | status               |       | ComplianceCheck   |
+-------------------+       | created_at           |       +-------------------+
                            | updated_at           |       | id (PK)           |
                            +----------------------+       | loan_id (FK)      |
                                      ^                    | check_type        |
                                      |                    | status            |
                            +---------+---------+          | notes             |
                            |                   |          | created_at        |
                            |                   |          | updated_at        |
                    +---------------+    +---------------+ +-------------------+
                    | LoanDocument  |    | AuditTrail    |
                    +---------------+    +---------------+
                    | id (PK)       |    | id (PK)       |
                    | loan_id (FK)  |    | action        |
                    | document_type |    | entity_type   |
                    | file          |    | entity_id     |
                    | uploaded_at   |    | previous_state|
                    +---------------+    | new_state     |
                                         | performed_by  |
                                         | timestamp     |
                                         +---------------+
```

## Tables Description

### CustomUser

Extends Django's built-in User model to store additional user information.

| Field         | Type         | Description                           |
|---------------|--------------|---------------------------------------|
| id            | Integer      | Primary key                           |
| username      | String       | Unique username                       |
| email         | String       | User's email address                  |
| first_name    | String       | User's first name                     |
| last_name     | String       | User's last name                      |
| phone_number  | String       | User's phone number                   |
| is_active     | Boolean      | Whether the user account is active    |
| is_staff      | Boolean      | Whether the user is a staff member    |
| date_joined   | DateTime     | When the user joined                  |
| last_login    | DateTime     | When the user last logged in          |

### LoanApplication

Stores information about loan applications submitted by users.

| Field             | Type         | Description                           |
|-------------------|--------------|---------------------------------------|
| id                | Integer      | Primary key                           |
| user_id           | Integer      | Foreign key to CustomUser             |
| loan_amount       | Decimal      | Amount of loan requested              |
| loan_purpose      | String       | Purpose of the loan                   |
| loan_term_months  | Integer      | Loan term in months                   |
| employment_status | String       | Employment status (EMPLOYED, etc.)    |
| annual_income     | Decimal      | Annual income of the applicant        |
| address           | Text         | Address of the applicant              |
| existing_loans    | Integer      | Number of existing loans              |
| status            | String       | Status (PENDING, APPROVED, REJECTED)  |
| created_at        | DateTime     | When the application was created      |
| updated_at        | DateTime     | When the application was last updated |

### CreditScore

Stores credit score information for loan applications.

| Field          | Type         | Description                           |
|----------------|--------------|---------------------------------------|
| id             | Integer      | Primary key                           |
| loan_id        | Integer      | Foreign key to LoanApplication        |
| score          | Integer      | Credit score (300-850)                |
| risk_category  | String       | Risk category (LOW, MEDIUM, HIGH)     |
| calculated_at  | DateTime     | When the score was calculated         |
| factors        | JSON         | Factors used in score calculation     |

### LoanDocument

Stores documents uploaded for loan applications.

| Field          | Type         | Description                           |
|----------------|--------------|---------------------------------------|
| id             | Integer      | Primary key                           |
| loan_id        | Integer      | Foreign key to LoanApplication        |
| document_type  | String       | Type of document (INCOME_PROOF, etc.) |
| file           | File         | Uploaded file                         |
| uploaded_at    | DateTime     | When the document was uploaded        |

### ComplianceCheck

Stores compliance check information for loan applications.

| Field          | Type         | Description                           |
|----------------|--------------|---------------------------------------|
| id             | Integer      | Primary key                           |
| loan_id        | Integer      | Foreign key to LoanApplication        |
| check_type     | String       | Type of check (IDENTITY, AML, etc.)   |
| status         | String       | Status (PENDING, PASSED, FAILED)      |
| notes          | Text         | Notes about the check                 |
| created_at     | DateTime     | When the check was created            |
| updated_at     | DateTime     | When the check was last updated       |

### AuditTrail

Stores audit trail information for tracking changes.

| Field           | Type         | Description                           |
|-----------------|--------------|---------------------------------------|
| id              | Integer      | Primary key                           |
| action          | String       | Action (CREATE, UPDATE, DELETE)       |
| entity_type     | String       | Type of entity (LOAN, CHECK, etc.)    |
| entity_id       | Integer      | ID of the entity                      |
| previous_state  | JSON         | Previous state of the entity          |
| new_state       | JSON         | New state of the entity               |
| performed_by    | Integer      | Foreign key to CustomUser             |
| timestamp       | DateTime     | When the action was performed         |

## Relationships

- **CustomUser to LoanApplication**: One-to-Many (A user can have multiple loan applications)
- **LoanApplication to CreditScore**: One-to-Many (A loan application can have multiple credit scores, e.g., after rescoring)
- **LoanApplication to LoanDocument**: One-to-Many (A loan application can have multiple documents)
- **LoanApplication to ComplianceCheck**: One-to-Many (A loan application can have multiple compliance checks)
- **CustomUser to AuditTrail**: One-to-Many (A user can perform multiple actions that are tracked in the audit trail)

## Indexes

The following indexes are recommended for optimal performance:

- `CustomUser.email` (for email lookups)
- `LoanApplication.user_id` (for finding a user's loans)
- `LoanApplication.status` (for filtering by status)
- `CreditScore.loan_id` (for finding scores for a loan)
- `LoanDocument.loan_id` (for finding documents for a loan)
- `ComplianceCheck.loan_id` (for finding compliance checks for a loan)
- `AuditTrail.entity_type` and `AuditTrail.entity_id` (for finding audit trail entries for an entity)