import React from 'react';
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';

import RegisterForm from './users/RegisterForm';
import LoginForm from './users/LoginForm';
import Profile from './users/Profile';
import Navbar from './users/Navbar';
import LoanSubmitForm from './loans/LoanSubmitForm';
import MyLoanList from './loans/MyLoanList';
import LoanDetail from './loans/LoanDetail';
import ScoreViewer from './credit/ScoreViewer';
import AdminScoreList from './credit/AdminScoreList';
import AdminScoreDetail from './credit/AdminScoreDetail';
import PrivateRoute from './users/PrivateRoute';
import LoanDocumentUpload from "./loans/LoanDocumentUpload";
import RescoreButton from "./credit/RescoreButton";
import RiskSnapshotList from './risk_dashboard/RiskSnapshotList';
import RiskTrendChart from './risk_dashboard/RiskTrendChart';
import ModelPerformanceLog from './risk_dashboard/ModelPerformanceLog';
import LoanComplianceChecks from './compliance/LoanComplianceChecks';
import ComplianceCheckUpdate from './compliance/ComplianceCheckUpdate';
import ComplianceAuditTrail from './compliance/ComplianceAuditTrail';
import MockKYCViewer from './integrations/MockKYCViewer';
import MockExperianViewer from './integrations/MockExperianViewer';
import AdminMockExperianList from './integrations/AdminMockExperianList';

// console.log(RegisterForm);

function App() {
    return (
        <Router>
            <Navbar/>

            <div className="min-h-screen bg-gray-100 p-4">
                <Routes>
                    <Route path="/register" element={<RegisterForm/>}/>
                    <Route path="/login" element={<LoginForm/>}/>
                    <Route path="/profile" element={<Profile/>}/>
                    <Route path={"/private"} element={<PrivateRoute/>} />
                    <Route path="/loans/apply" element={<LoanSubmitForm />} />
                    <Route path="/loans" element={<MyLoanList />} />
                    <Route path="/loans/:id" element={<LoanDetail />} />
                    <Route path="/document/upload/" element={<LoanDocumentUpload />} />
                    <Route path="/score/loan/:loan_id" element={<ScoreViewer />} />
                    <Route path="/rescore" element={<RescoreButton/>} />
                    <Route path="/admin/scores" element={<AdminScoreList />} />
                    <Route path="/admin/scores/:id" element={<AdminScoreDetail />} />
                    <Route path="/risk/snapshots" element={<PrivateRoute><RiskSnapshotList /></PrivateRoute>} />
                    <Route path="/risk/trends" element={<PrivateRoute><RiskTrendChart /></PrivateRoute>} />
                    <Route path="/risk/models" element={<PrivateRoute><ModelPerformanceLog /></PrivateRoute>} />
                    <Route path="/compliance/loan/:loanId" element={<PrivateRoute><LoanComplianceChecks /></PrivateRoute>} />
                    <Route path="/compliance/check/:id/edit" element={<PrivateRoute><ComplianceCheckUpdate /></PrivateRoute>} />
                    <Route path="/compliance/audit-trail" element={<PrivateRoute><ComplianceAuditTrail /></PrivateRoute>} />
                    <Route path="/mock/kyc" element={<PrivateRoute><MockKYCViewer /></PrivateRoute>} />
                    <Route path="/mock/experian/:loanId" element={<PrivateRoute><MockExperianViewer /></PrivateRoute>} />
                    <Route path="/mock/experian/all" element={<PrivateRoute><AdminMockExperianList /></PrivateRoute>} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;

