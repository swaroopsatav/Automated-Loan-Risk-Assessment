import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import scoreAPI from './scoreApi';

const AdminScoreList = () => {
  const [scores, setScores] = useState([]);

  useEffect(() => {
    scoreAPI.get('admin/scores/').then(res => setScores(res.data));
  }, []);

  return (
    <div className="p-4">
      <h2 className="text-xl font-semibold mb-4">All Credit Scores</h2>
      <ul className="space-y-2">
        {scores.map(score => (
          <li key={score.id} className="bg-white p-3 rounded shadow">
            <Link to={`/admin/scores/${score.id}`} className="font-medium text-blue-600">
              Loan #{score.loan_id} — {score.user}
            </Link>
            <p>Risk: {score.risk_score} | Decision: {score.decision}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AdminScoreList;
