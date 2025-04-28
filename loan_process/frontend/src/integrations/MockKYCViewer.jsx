import React, { useEffect, useState } from 'react';
import integrationsAPI from './api';

const MockKYCViewer = () => {
  const [kyc, setKyc] = useState(null);

  useEffect(() => {
    integrationsAPI.get('mock/kyc/').then(res => setKyc(res.data));
  }, []);

  if (!kyc) return <p>Loading...</p>;

  return (
    <div className="p-4 bg-white max-w-md mx-auto rounded shadow">
      <h2 className="text-xl font-bold mb-2">Mock KYC Record</h2>
      <p><strong>PAN:</strong> {kyc.pan_number} ({kyc.pan_verified ? '✔ Verified' : '❌'})</p>
      <p><strong>Aadhaar Last 4:</strong> {kyc.aadhaar_last_4} ({kyc.aadhaar_verified ? '✔ Verified' : '❌'})</p>
      <p><strong>DOB:</strong> {kyc.dob}</p>
      <p><strong>KYC Type:</strong> {kyc.kyc_type}</p>
      <pre className="text-sm bg-gray-100 mt-3 p-2 rounded overflow-x-auto">
        {JSON.stringify(kyc.mock_response, null, 2)}
      </pre>
    </div>
  );
};

export default MockKYCViewer;
