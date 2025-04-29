import React, { useState } from 'react';
import API from './api.js';
import { useNavigate } from 'react-router-dom';

const RegisterForm = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    password2: '',
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

  // Handle input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  // Handle file changes
  const handleFileChange = (e) => {
    const { name, files } = e.target;
    setDocuments((prev) => ({ ...prev, [name]: files[0] }));
  };

  // Validate form data
  const validateForm = () => {
    if (formData.password !== formData.password2) {
      setMessage('Passwords do not match.');
      return false;
    }
    if (!formData.email.includes('@')) {
      setMessage('Invalid email format.');
      return false;
    }
    if (!formData.phone_number.match(/^\d{10}$/)) {
      setMessage('Phone number must be 10 digits.');
      return false;
    }
    return true;
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    if (!validateForm()) return;

    setIsSubmitting(true);

    const form = new FormData();
    Object.entries(formData).forEach(([key, value]) => form.append(key, value));
    Object.entries(documents).forEach(([key, file]) => {
      if (file) form.append(key, file);
    });

    try {
      const response = await API.post('api/users/auth/register/', form, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log('Registration response:', response);
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

  // Reusable input component
  const renderInput = (label, name, type = 'text', placeholder = '', required = false) => (
    <div>
      <label className="block text-gray-700">{label}:</label>
      <input
        className="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
        name={name}
        type={type}
        placeholder={placeholder}
        value={formData[name]}
        onChange={handleChange}
        required={required}
      />
    </div>
  );

  return (
    <form onSubmit={handleSubmit} className="p-6 max-w-xl mx-auto bg-white shadow-md rounded-lg space-y-6">
      <h2 className="text-2xl font-bold text-gray-800 text-center">REGISTRATION</h2>
      {message && (
        <div
          className={`${
            message.includes('successful') ? 'text-green-500' : 'text-red-500'
          } text-sm text-center`}
          aria-live="polite"
        >
          {message}
        </div>
      )}

      {renderInput('Username', 'username', 'text', 'Username', true)}
      {renderInput('Email', 'email', 'email', 'Email', true)}
      {renderInput('Password', 'password', 'password', 'Password', true)}
      {renderInput('Confirm Password', 'password2', 'password', 'Confirm Password', true)}
      {renderInput('Phone Number', 'phone_number', 'text', 'Phone Number')}
      {renderInput('Date of Birth', 'date_of_birth', 'date')}
      {renderInput('Address', 'address', 'text', 'Address')}
      {renderInput('Annual Income', 'annual_income', 'number', 'Annual Income')}
      {renderInput('Employment Status', 'employment_status', 'text', 'Employment Status')}
      {renderInput('ID Type', 'govt_id_type', 'text', 'ID Type')}
      {renderInput('ID Number', 'govt_id_number', 'text', 'ID Number')}

      <div className="space-y-4">
        <label className="block text-gray-700">ID Proof:</label>
        <input
          className="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
          type="file"
          name="id_proof"
          onChange={handleFileChange}
        />
        <label className="block text-gray-700">Address Proof:</label>
        <input
          className="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
          type="file"
          name="address_proof"
          onChange={handleFileChange}
        />
        <label className="block text-gray-700">Income Proof:</label>
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