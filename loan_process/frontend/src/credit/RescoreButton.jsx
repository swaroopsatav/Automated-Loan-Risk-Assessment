// RescoreButton.jsx
import React, { useState } from 'react';
import scoreAPI from './scoreApi';

const RescoreButton = ({ loanId }) => {
  const [msg, setMsg] = useState('');

  const handleRescore = async () => {
    try {
      await scoreAPI.post(`admin/rescore/${loanId}/`);
      setMsg('✅ Loan re-scored successfully.');
    } catch (err) {
      setMsg('❌ Failed to re-score loan.');
    }
  };

  return (
    <div>
      <button onClick={handleRescore} className="bg-yellow-500 text-white px-3 py-1 rounded">
        Rescore Loan
      </button>
      {msg && <p className="text-sm mt-1">{msg}</p>}
    </div>
  );
};

export default RescoreButton;
