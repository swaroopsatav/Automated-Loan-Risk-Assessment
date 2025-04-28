import React, { useEffect, useState } from 'react';
import integrationsAPI from './api';
import { Link } from 'react-router-dom';

const AdminMockExperianList = () => {
  const [reports, setReports] = useState([]);

  useEffect(() => {
    integrationsAPI.get('mock/experian/all/').then(res => setReports(res.data));
  }, []);

  return (
    <div className="p-4 max-w-5xl mx-auto">
      <h2 className="text-xl font-bold mb-4">All Mock Experian Reports</h2>
      <table className="table-auto w-full text-sm">
        <thead className="bg-gray-200 text-left">
          <tr>
            <th>User</th>
            <th>Loan</th>
            <th>Score</th>
            <th>Utilization</th>
            <th>Overdue</th>
            <th>Created</th>
          </tr>
        </thead>
        <tbody>
          {reports.map(r => (
            <tr key={r.id} className="border-t">
              <td>{r.user}</td>
              <td><Link to={`/mock/experian/${r.loan_application}`}>#{r.loan_application}</Link></td>
              <td>{r.bureau_score}</td>
              <td>{r.credit_utilization_pct}%</td>
              <td>{r.overdue_accounts}</td>
              <td>{new Date(r.created_at).toLocaleDateString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AdminMockExperianList;
