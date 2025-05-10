# Loan Processing System Frontend

This is the React frontend for the Loan Processing System. It provides a user-friendly interface for users to submit loan applications, track their status, upload documents, and more.

## Features

- User registration and login
- Dashboard for viewing loan applications
- Loan application submission form
- Document upload functionality
- Status tracking for loan applications
- Admin dashboard for loan management
- Credit score visualization
- Compliance check management

## Technology Stack

- React 18+
- Vite for build tooling and development server
- React Router for navigation
- Axios for API communication
- React Hook Form for form handling
- Chart.js for data visualization
- Tailwind CSS for styling

## Project Structure

```
frontend/
├── public/            # Static assets
├── src/
│   ├── api/           # API integration
│   ├── assets/        # Images, fonts, etc.
│   ├── components/    # Reusable components
│   │   ├── common/    # Common UI components
│   │   ├── forms/     # Form components
│   │   └── layout/    # Layout components
│   ├── contexts/      # React contexts
│   ├── hooks/         # Custom hooks
│   ├── pages/         # Page components
│   ├── routes/        # Route definitions
│   ├── services/      # Business logic
│   ├── utils/         # Utility functions
│   ├── App.jsx        # Main application component
│   └── main.jsx       # Entry point
├── .eslintrc.cjs      # ESLint configuration
├── index.html         # HTML template
├── package.json       # Dependencies and scripts
└── vite.config.js     # Vite configuration
```

## Getting Started

1. Make sure the backend server is running
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
4. Open your browser and navigate to `http://localhost:5173`

## Available Scripts

- `npm run dev` - Start the development server
- `npm run build` - Build for production
- `npm run lint` - Run ESLint
- `npm run preview` - Preview the production build locally

## API Integration

The frontend communicates with the backend API using Axios. API calls are organized in the `src/api` directory, with separate modules for different API endpoints:

- `auth.js` - Authentication API calls
- `loans.js` - Loan application API calls
- `documents.js` - Document upload API calls
- `credit.js` - Credit score API calls
- `compliance.js` - Compliance check API calls

## Authentication

The frontend uses JWT authentication. The authentication flow is handled by the `AuthContext` provider, which manages the user's authentication state and provides login/logout functionality to all components.

## Deployment

To deploy the frontend:

1. Build the production version:
   ```bash
   npm run build
   ```
2. The build output will be in the `dist` directory
3. Deploy the contents of the `dist` directory to your web server or hosting service

## Development Guidelines

- Follow the component structure: Each component should be in its own directory with index.js for export
- Use functional components and hooks instead of class components
- Use React Router for navigation
- Use React Context for global state management
- Follow the ESLint rules for code quality
