# Compliances Module Synchronization

This directory contains utility functions for ensuring the compliances module is properly synchronized with other modules in both the frontend and backend.

## Backend Synchronization

The `async_utils.py` file provides asynchronous utility functions that allow the compliances module to work seamlessly with other modules that use asynchronous operations. These functions use Django's `asgiref.sync` module to convert synchronous database operations to asynchronous ones.

### Available Functions

- `get_compliance_checks_async(loan_id)`: Asynchronously retrieve compliance checks for a loan
- `get_compliance_check_async(check_id)`: Asynchronously retrieve a specific compliance check
- `update_compliance_check_async(check_id, data, user)`: Asynchronously update a compliance check and create an audit trail
- `get_audit_trail_async(loan_id=None)`: Asynchronously retrieve compliance audit trail entries

### Usage

These functions are used in the views.py file to ensure that API endpoints handle requests asynchronously, which is consistent with how other modules in the application work.

Example:
```python
async def get_queryset(self):
    loan_id = self.kwargs.get('loan_id')
    return await get_compliance_checks_async(loan_id)
```

## Frontend Synchronization

The frontend already uses a shared API utility (`apiUtils.js`) that creates separate API instances for each module, ensuring proper synchronization. The compliances module's frontend components use this shared utility through `api.js`.

### Key Components

- `api.js`: Creates a compliance-specific API instance using the shared utility
- `ComplianceAuditTrail.jsx`: Component for displaying audit trails
- `ComplianceCheckUpdate.jsx`: Component for updating compliance checks
- `LoanComplianceChecks.jsx`: Component for displaying compliance checks for a loan

## Synchronization Strategy

1. **Backend**: Use async/await pattern with Django's ASGI support
2. **Frontend**: Use module-specific API instances created from a shared utility

This approach ensures that the compliances module is properly synchronized with other modules in both the frontend and backend parts of the application.