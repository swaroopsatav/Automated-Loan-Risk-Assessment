import React, { useState } from 'react';
import { loginUser } from './auth';
import { useNavigate } from 'react-router-dom';

const LoginForm = () => {
    const [form, setForm] = useState({ username: '', password: '' });
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false); // Loading state
    const navigate = useNavigate();

    // Handle input changes
    const handleChange = (e) => {
        const { name, value } = e.target;
        setForm((prevState) => ({ ...prevState, [name]: value.trim() }));
    };

    // Handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(''); // Clear previous errors
        setIsLoading(true); // Show loading indicator

        try {
            const response = await loginUser(form);
            if (response.success) {
                navigate('/profile'); // Redirect to the profile page on success
            } else {
                setError(response.message); // Show a server-side error message
            }
            // eslint-disable-next-line no-unused-vars
        } catch (err) {
            setError('Unable to connect to the server. Please try again later.');
        } finally {
            setIsLoading(false); // Hide loading indicator
        }
    };

    return (
        <form
            onSubmit={handleSubmit}
            className="p-8 max-w-md mx-auto bg-white shadow-md rounded-lg border border-gray-200"
        >
            <h2 className="text-2xl font-bold mb-4 text-center text-gray-800">LOGIN</h2>
            {error && (
                <p className="text-red-600 text-center mb-4 border border-red-400 bg-red-100 p-2 rounded-lg">
                    {error}
                </p>
            )}
            <div className="mb-4">
                <input
                    type="text"
                    name="username"
                    value={form.username}
                    onChange={handleChange}
                    placeholder="Username"
                    required
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
            </div>
            <div className="mb-4">
                <input
                    type="password"
                    name="password"
                    value={form.password}
                    onChange={handleChange}
                    placeholder="Password"
                    required
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
            </div>
            <button
                type="submit"
                disabled={isLoading} // Disable button during loading
                className={`w-full px-4 py-2 rounded-lg transition duration-300 ${
                    isLoading
                        ? 'bg-gray-400 cursor-not-allowed'
                        : 'bg-blue-500 text-white hover:bg-blue-600'
                }`}
            >
                {isLoading ? 'Logging in...' : 'Login'} {/* Show loading text */}
            </button>
        </form>
    );
};

export default LoginForm;