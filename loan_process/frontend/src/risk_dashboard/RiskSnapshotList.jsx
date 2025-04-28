import React, { useEffect, useState } from 'react';
import riskAPI from './api';

const RiskSnapshotList = () => {
  const [snapshots, setSnapshots] = useState([]);

  useEffect(() => {
    riskAPI.get('risk/snapshots/').then(res => setSnapshots(res.data));
  }, []);

  return (
    <div className="p-4 max-w-4xl mx-auto space-y-4">
      <h2 className="text-xl font-bold">Risk Snapshots</h2>
      {snapshots.map(snapshot => (
        <div key={snapshot.id} className="bg-white p-4 rounded shadow">
          <h3 className="font-semibold">Snapshot: {snapshot.snapshot_date}</h3>
          <p>Total Applications: {snapshot.total_applications}</p>
          <p>Average Score: {snapshot.avg_risk_score}</p>
          <p>Approved: {snapshot.approved_count}, Rejected: {snapshot.rejected_count}</p>
          <p>High Risk: {snapshot.high_risk_count}, Low Risk: {snapshot.low_risk_count}</p>
        </div>
      ))}
    </div>
  );
};

export default RiskSnapshotList;
