import React, { useEffect, useState } from 'react';
import riskAPI from './api';

const ModelPerformanceLog = () => {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    riskAPI.get('risk/models/').then(res => setLogs(res.data));
  }, []);

  return (
    <div className="p-4 max-w-5xl mx-auto">
      <h2 className="text-xl font-bold mb-4">Model Performance Logs</h2>
      <table className="w-full table-auto text-sm border">
        <thead className="bg-gray-100">
          <tr>
            <th>Model</th><th>Accuracy</th><th>Precision</th><th>Recall</th><th>AUC</th><th>Date</th>
          </tr>
        </thead>
        <tbody>
          {logs.map(log => (
            <tr key={log.id} className="text-center border-t">
              <td>{log.model_version}</td>
              <td>{log.accuracy}</td>
              <td>{log.precision}</td>
              <td>{log.recall}</td>
              <td>{log.auc_score}</td>
              <td>{new Date(log.timestamp).toLocaleDateString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ModelPerformanceLog;
