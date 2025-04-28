import React, { useState } from 'react';
import loanAPI from './api';

const LoanDocumentUpload = ({ loanId }) => {
  const [form, setForm] = useState({ document_type: '', file: null });
  const [msg, setMsg] = useState('');

  const handleChange = e => {
    const { name, value, files } = e.target;
    setForm(prev => ({ ...prev, [name]: files ? files[0] : value }));
  };

  const handleSubmit = async e => {
    e.preventDefault();
    const data = new FormData();
    data.append('loan', loanId);
    data.append('document_type', form.document_type);
    data.append('file', form.file);
    try {
      await loanAPI.post('loans/documents/', data);
      setMsg('Uploaded successfully!');
    } catch {
      setMsg('Upload failed.');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-2">
      <input type="text" name="document_type" placeholder="e.g. Bank Statement" onChange={handleChange} required />
      <input type="file" name="file" onChange={handleChange} required />
      <button type="submit" className="bg-blue-600 text-white px-3 py-1 rounded">Upload</button>
      {msg && <p>{msg}</p>}
    </form>
  );
};

export default LoanDocumentUpload;
