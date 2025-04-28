import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import integrationsAPI from './api';

const MockExperianViewer = () => {
  const { loanId } = useParams();
  const [report, setReport] = useState(null);

  useEffect(() => {
    integrationsAPI.get(`mock/experian/${loanId}/`).then(res => setReport(res.data));
  }, [loanId]);

  if (!report) return <p>Loading...</p>;

  return (
    <div className="p-4 bg-white max-w-3xl mx-auto rounded shadow">
      <h2 className="text-xl font-bold mb-2">Mock Experian Report</h2>
      <p><strong>Bureau Score:</strong> {report.bureau_score} ({report.score_band})</p>
      <p><strong>Accounts:</strong> {report.total_accounts} total, {report.active_accounts} active</p>
      <p><strong>Overdue:</strong> {report.overdue_accounts} overdue, DPD max: {report.dpd_max} days</p>
      <p><strong>Utilization:</strong> {report.credit_utilization_pct}%</p>
      <p><strong>EMI/Income Ratio:</strong> {report.emi_to_income_ratio}</p>

      <h4 className="font-semibold mt-4">Raw Report</h4>
      <pre className="text-sm bg-gray-100 mt-2 p-2 rounded overflow-x-auto">
        {JSON.stringify(report.mock_raw_report, null, 2)}
      </pre>
    </div>
  );
};

export default MockExperianViewer;
