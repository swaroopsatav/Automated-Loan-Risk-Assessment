import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import scoreAPI from './scoreApi';

const ScoreViewer = () => {
  const { loan_id } = useParams();
  const [score, setScore] = useState(null);
    score.scoring_output = undefined;
    score.scoring_inputs = undefined;
    score.decision = undefined;
    score.risk_score = undefined;
    score.loan_id = undefined;

  useEffect(() => {
    scoreAPI.get(`score/loan/${loan_id}/`).then(res => setScore(res.data));
  }, [loan_id]);

  if (!score) return <p className="p-4">Loading...</p>;

  return (
    <div className="max-w-xl mx-auto bg-white shadow p-4 rounded">
      <h2 className="text-lg font-semibold mb-2">Credit Score for Loan #{score.loan_id}</h2>
      <p><strong>Risk Score:</strong> {score.risk_score}</p>
      <p><strong>Decision:</strong> {score.decision}</p>
      <p><strong>Model:</strong> {score.model_name}</p>
      <h4 className="mt-4 font-medium">Inputs</h4>
      <pre className="bg-gray-100 p-2 rounded text-sm">{JSON.stringify(score.scoring_inputs, null, 2)}</pre>
      <h4 className="mt-2 font-medium">Output / Explanation</h4>
      <pre className="bg-gray-100 p-2 rounded text-sm">{JSON.stringify(score.scoring_output, null, 2)}</pre>
    </div>
  );
};

export default ScoreViewer;
