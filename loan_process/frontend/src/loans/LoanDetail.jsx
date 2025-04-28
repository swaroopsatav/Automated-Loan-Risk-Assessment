import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import loanAPI from './api';

const LoanDetail = () => {
  const { id } = useParams();
  const [loan, setLoan] = useState(null);

  useEffect(() => {
    loanAPI.get(`loans/mine/${id}/`).then(res => setLoan(res.data));
  }, [id]);

  if (!loan) return <p className="p-4">Loading...</p>;

  return (
    <div className="p-4 max-w-2xl mx-auto space-y-2 bg-white shadow rounded">
      <h2 className="text-xl font-semibold">Loan #{loan.id}</h2>
      <p><strong>Status:</strong> {loan.status}</p>
      <p><strong>Risk Score:</strong> {loan.risk_score}</p>
      <p><strong>AI Decision:</strong> {loan.ai_decision}</p>
      <p><strong>Purpose:</strong> {loan.purpose}</p>
      <p><strong>Scoring Breakdown:</strong></p>
      <pre className="bg-gray-100 p-2 rounded text-sm">{JSON.stringify(loan.ml_scoring_output, null, 2)}</pre>

      <h4 className="font-medium mt-4">Documents</h4>
      <ul className="list-disc list-inside">
        {loan.documents?.map(doc => (
          <li key={doc.id}>
            <a href={doc.file} target="_blank" rel="noopener noreferrer" className="text-blue-600">
              {doc.document_type}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default LoanDetail;
