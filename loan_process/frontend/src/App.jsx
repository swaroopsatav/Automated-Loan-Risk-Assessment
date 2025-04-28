import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

// Importing user-related components
import RegisterForm from './users/RegisterForm';
import LoginForm from './users/LoginForm';
import Profile from './users/Profile';
import Navbar from './users/Navbar';
import PrivateRoute from './users/PrivateRoute';

// Importing loan-related components
import LoanSubmitForm from './loans/LoanSubmitForm';
import MyLoanList from './loans/MyLoanList';
import LoanDetail from './loans/LoanDetail';
import LoanDocumentUpload from './loans/LoanDocumentUpload';

// Importing credit-related components
import ScoreViewer from './credit/ScoreViewer';
import RescoreButton from './credit/RescoreButton';
import AdminScoreList from './credit/AdminScoreList';
import AdminScoreDetail from './credit/AdminScoreDetail';

// Importing risk dashboard components
import RiskSnapshotList from './risk_dashboard/RiskSnapshotList';
import RiskTrendChart from './risk_dashboard/RiskTrendChart';
import ModelPerformanceLog from './risk_dashboard/ModelPerformanceLog';

// Importing compliance components
import LoanComplianceChecks from './compliance/LoanComplianceChecks';
import ComplianceCheckUpdate from './compliance/ComplianceCheckUpdate';
import ComplianceAuditTrail from './compliance/ComplianceAuditTrail';

// Importing integration components
import MockKYCViewer from './integrations/MockKYCViewer';
import MockExperianViewer from './integrations/MockExperianViewer';
import AdminMockExperianList from './integrations/AdminMockExperianList';

const App = () => {
  return (
    <Router>
      {/* Navbar is always visible */}
      <Navbar />

      {/* Main content section */}
      <div className="min-h-screen bg-gray-100 p-4">
        <Routes>
          {/* User routes */}
          <Route path="/register" element={<RegisterForm />} />
          <Route path="/login" element={<LoginForm />} />
          <Route path="/profile" element={<Profile />} />

          {/* Loan routes */}
          <Route path="/loans/apply" element={<LoanSubmitForm />} />
          <Route path="/loans" element={<MyLoanList />} />
          <Route path="/loans/:id" element={<LoanDetail />} />
          <Route path="/document/upload" element={<LoanDocumentUpload />} />

          {/* Credit routes */}
          <Route path="/score/loan/:loan_id" element={<ScoreViewer />} />
          <Route path="/rescore" element={<RescoreButton />} />
          <Route path="/admin/scores" element={<AdminScoreList />} />
          <Route path="/admin/scores/:id" element={<AdminScoreDetail />} />

          {/* Risk dashboard routes */}
          <Route path="/risk/snapshots" element={<RiskSnapshotList />} />
          <Route path="/risk/trends" element={<RiskTrendChart />} />
          <Route path="/risk/models" element={<ModelPerformanceLog />} />

          {/* Compliance routes */}
          <Route path="/compliance/loan/:loanId" element={<LoanComplianceChecks />} />
          <Route path="/compliance/check/:id/edit" element={<ComplianceCheckUpdate />} />
          <Route path="/compliance/audit-trail" element={<ComplianceAuditTrail />} />

          {/* Integration routes */}
          <Route path="/mock/kyc" element={<MockKYCViewer />} />
          <Route path="/mock/experian/:loanId" element={<MockExperianViewer />} />
          <Route path="/mock/experian/all" element={<AdminMockExperianList />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;