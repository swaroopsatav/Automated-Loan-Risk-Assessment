// AdminScoreDetail.jsx
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import scoreAPI from './scoreApi';
import RescoreButton from './RescoreButton';

const AdminScoreDetail = () => {
  const { id } = useParams();
  const [score, setScore] = useState(null);

  useEffect(() => {
    scoreAPI.get(`admin/scores/${id}/`).then(res => setScore(res.data));
  }, [id]);

  if (!score) return <p>Loading...</p>;

  return (
    <div className="max-w-2xl mx-auto bg-white p-4 shadow rounded">
      <h2 className="text-lg font-semibold">Admin Score Detail</h2>
      <p><strong>User:</strong> {score.user}</p>
      <p><strong>Loan ID:</strong> {score.loan_id}</p>
      <p><strong>Model:</strong> {score.model_name}</p>
      <p><strong>Risk Score:</strong> {score.risk_score}</p>
      <p><strong>Decision:</strong> {score.decision}</p>
      <h4 className="mt-4 font-medium">Inputs</h4>
      <pre className="bg-gray-100 p-2 text-sm">{JSON.stringify(score.scoring_inputs, null, 2)}</pre>
      <h4 className="mt-2 font-medium">Explanation</h4>
      <pre className="bg-gray-100 p-2 text-sm">{JSON.stringify(score.scoring_output, null, 2)}</pre>
      <div className="mt-4">
        <RescoreButton loanId={score.loan_id} />
      </div>
    </div>
  );
};
export default AdminScoreDetail;
