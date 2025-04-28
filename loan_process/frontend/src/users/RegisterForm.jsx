import React, {useState} from 'react';
//import axios from 'axios';
import API from './api.js';
import {useNavigate} from 'react-router-dom'

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

  const handleChange = (e) => {
    const {name, value} = e.target;
    setFormData(prev => ({...prev, [name]: value}));
  };

  const handleFileChange = (e) => {
    const {name, files} = e.target;
    setDocuments(prev => ({...prev, [name]: files[0]}));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const form = new FormData();
    Object.entries(formData).forEach(([key, value]) => form.append(key, value));
    Object.entries(documents).forEach(([key, file]) => {
      if (file) form.append(key, file);
    });

    try {
      const res = await API.post('/api/register/', form, {
        headers: {'Content-Type': 'multipart/form-data'},
      });
      setMessage('Registration successful! Please log in.');
      navigate("/login");
    } catch (err) {
      console.error(err);
      setMessage('Something went wrong. Check your details.');
    }
  };

  return (
      <form onSubmit={handleSubmit} className="p-6 max-w-xl mx-auto bg-white shadow-md rounded-lg space-y-6">
          <h2 className="text-2xl font-bold text-gray-800 text-center">REGISTRATION</h2>
        {message && <div className="text-red-500 text-sm">{message}</div>}

        <input
            className="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
            name="username"
            placeholder="Username"
            onChange={handleChange}
            required
        />
        <input
            className="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
            name="email"
            type="email"
            placeholder="Email"
            onChange={handleChange}
            required
        />
        <input
            className="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
            name="password"
            type="password"
            placeholder="Password"
            onChange={handleChange}
            required
        />

        <input
            className="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
            name="phone_number"
            placeholder="Phone Number"
            onChange={handleChange}
        />
        <input
            className="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
            name="date_of_birth"
            type="date"
            onChange={handleChange}
        />
        <input
            className="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
            name="address"
            placeholder="Address"
            onChange={handleChange}
        />

        <input
            className="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
            name="annual_income"
            type="number"
            placeholder="Annual Income"
            onChange={handleChange}
        />
        <input
            className="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
            name="employment_status"
            placeholder="Employment Status"
            onChange={handleChange}
        />
        <input
            className="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
            name="govt_id_type"
            placeholder="ID Type"
            onChange={handleChange}
        />
        <input
            className="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
            name="govt_id_number"
            placeholder="ID Number"
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
            className="w-full bg-indigo-500 text-white py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-indigo-400 hover:bg-indigo-600"
            type="submit"
        >
          Register
        </button>
      </form>
  );
};

export default RegisterForm;
