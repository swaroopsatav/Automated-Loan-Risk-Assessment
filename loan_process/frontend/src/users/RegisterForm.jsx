import React, { useState } from 'react';
import API from './api.js';
import { useNavigate } from 'react-router-dom';

const RegisterForm = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    phone_number: '',
    date_of_birth: '',
    address: '',
    annual_income: '',
    employment_status: '',
    govt_id_type: '',
    govt_id_number: '',
  });

  const [documents, setDocuments] = useState({
    id_proof: null,
    address_proof: null,
    income_proof: null,
  });

  const [message, setMessage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleFileChange = (e) => {
    const { name, files } = e.target;
    setDocuments((prev) => ({ ...prev, [name]: files[0] }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setMessage('');

    const form = new FormData();
    Object.entries(formData).forEach(([key, value]) => form.append(key, value));
    Object.entries(documents).forEach(([key, file]) => {
      if (file) form.append(key, file);
    });

    try {
      const response = await API.post('/api/register/', form, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setMessage('Registration successful! Redirecting to login...');
      setTimeout(() => navigate('/login'), 2000); // Redirect after 2 seconds
    } catch (err) {
      console.error('Registration error:', err);
      if (err.response && err.response.data) {
        // Display server validation errors
        setMessage(err.response.data.detail || 'Something went wrong. Check your details and try again.');
      } else {
        setMessage('Something went wrong. Please try again later.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-6 max-w-xl mx-auto bg-white shadow-md rounded-lg space-y-6">
      <h2 className="text-2xl font-bold text-gray-800 text-center">REGISTRATION</h2>
      {message && <div className={`${message.includes('successful') ? 'text-green-500' : 'text-red-500'} text-sm`}>{message}</div>}

      <input
        className="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
        name="username"
        placeholder="Username"
        value={formData.username}
        onChange={handleChange}
        required
      />
      <input
        className="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
        name="email"
        type="email"
        placeholder="Email"
        value={formData.email}
        onChange={handleChange}
        required
      />
      <input
        className="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
        name="password"
        type="password"
        placeholder="Password"
        value={formData.password}
        onChange={handleChange}
        required
      />

      <input
        className="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
        name="phone_number"
        placeholder="Phone Number"
        value={formData.phone_number}
        onChange={handleChange}
      />
      <input
        className="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
        name="date_of_birth"
        type="date"
        value={formData.date_of_birth}
        onChange={handleChange}
      />
      <input
        className="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
        name="address"
        placeholder="Address"
        value={formData.address}
        onChange={handleChange}
      />

      <input
        className="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
        name="annual_income"
        type="number"
        placeholder="Annual Income"
        value={formData.annual_income}
        onChange={handleChange}
      />
      <input
        className="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
        name="employment_status"
        placeholder="Employment Status"
        value={formData.employment_status}
        onChange={handleChange}
      />
      <input
        className="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
        name="govt_id_type"
        placeholder="ID Type"
        value={formData.govt_id_type}
        onChange={handleChange}
      />
      <input
        className="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
        name="govt_id_number"
        placeholder="ID Number"
        value={formData.govt_id_number}
        onChange={handleChange}
      />

      <div className="space-y-2">
        <label className="block text-gray-700">ID Proof</label>
        <input
          className="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
          type="file"
          name="id_proof"
          onChange={handleFileChange}
        />
      </div>
      <div className="space-y-2">
        <label className="block text-gray-700">Address Proof</label>
        <input
          className="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
          type="file"
          name="address_proof"
          onChange={handleFileChange}
        />
      </div>
      <div className="space-y-2">
        <label className="block text-gray-700">Income Proof</label>
        <input
          className="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
          type="file"
          name="income_proof"
          onChange={handleFileChange}
        />
      </div>

      <button
        className={`w-full bg-indigo-500 text-white py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-indigo-400 hover:bg-indigo-600 ${
          isSubmitting ? 'opacity-50 cursor-not-allowed' : ''
        }`}
        type="submit"
        disabled={isSubmitting}
      >
        {isSubmitting ? 'Registering...' : 'Register'}
      </button>
    </form>
  );
};

export default RegisterForm;