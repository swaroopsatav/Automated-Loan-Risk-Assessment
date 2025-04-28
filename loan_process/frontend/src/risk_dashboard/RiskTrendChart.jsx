import React, { useEffect, useState } from 'react';
import riskAPI from './api';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip);

const RiskTrendChart = () => {
  const [trendData, setTrendData] = useState([]);

  useEffect(() => {
    riskAPI.get('risk/trends/').then(res => setTrendData(res.data));
  }, []);

  const chartData = {
    labels: trendData.map(t => t.date),
    datasets: [
      {
        label: 'Avg Risk Score',
        data: trendData.map(t => t.avg_score),
        borderColor: 'blue',
        fill: false,
      },
      {
        label: 'Approval Rate',
        data: trendData.map(t => t.approval_rate),
        borderColor: 'green',
        fill: false,
      },
      {
        label: 'Rejection Rate',
        data: trendData.map(t => t.rejection_rate),
        borderColor: 'red',
        fill: false,
      },
    ],
  };

  return (
    <div className="p-4 max-w-5xl mx-auto">
      <h2 className="text-xl font-bold mb-4">Risk Trend Over Time</h2>
      <Line data={chartData} />
    </div>
  );
};

export default RiskTrendChart;
