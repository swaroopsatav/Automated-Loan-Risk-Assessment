import React, { useEffect, useState } from 'react';
import complianceAPI from './api';
import { useParams, useNavigate } from 'react-router-dom';

const ComplianceCheckUpdate = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [form, setForm] = useState({ status: '', reviewed_by: '', reviewed_at: '', notes: '' });

  useEffect(() => {
    // Prefill check (optional, or use admin-only info)
    complianceAPI.get(`compliance/loan/`).then(() => {}); // preload info if needed
  }, [id]);

  const handleChange = e => {
    const { name, value } = e.target;
    setForm(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      await complianceAPI.patch(`compliance/check/${id}/update/`, form);
      navigate(-1); // go back
    } catch {
      alert('Failed to update compliance check.');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-md mx-auto bg-white shadow p-4 space-y-4 rounded">
      <h2 className="text-xl font-semibold">Update Compliance Check</h2>
      <select name="status" onChange={handleChange} required className="w-full border p-2">
        <option value="">-- Select Status --</option>
        <option value="passed">Passed</option>
        <option value="flagged">Flagged</option>
        <option value="failed">Failed</option>
      </select>
      <input name="reviewed_by" placeholder="Staff user ID" onChange={handleChange} required className="w-full border p-2" />
      <input type="datetime-local" name="reviewed_at" onChange={handleChange} required className="w-full border p-2" />
      <textarea name="notes" rows={3} placeholder="Notes" onChange={handleChange} className="w-full border p-2" />
      <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">Update Check</button>
    </form>
  );
};

export default ComplianceCheckUpdate;
