import React, {useState} from 'react';
import {loginUser} from './auth';
import {useNavigate} from 'react-router-dom';

const LoginForm = () => {
    const [form, setForm] = useState({username: '', password: ''});
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleChange = e => setForm({...form, [e.target.name]: e.target.value});

    const handleSubmit = async (e) => {
        e.preventDefault();
        const data = await loginUser(form);
        if (data.access) navigate('/profile');
        else setError('Login failed.');
    };

    return (
        <form onSubmit={handleSubmit}
              className="p-8 max-w-md mx-auto bg-white shadow-md rounded-lg border border-gray-200">
            <h2 className="text-2xl font-bold mb-4 text-center text-gray-800">LOGIN</h2>
            {error && <p className="text-red-600 text-center mb-4">{error}</p>}
            <div className="mb-4">
                <input
                    type="text"
                    name="username"
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
                    onChange={handleChange}
                    placeholder="Password"
                    required
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
            </div>
            <button
                type="submit"
                className="w-full bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition duration-300"
            >
                Login
            </button>
        </form>
    );
};

export default LoginForm;
