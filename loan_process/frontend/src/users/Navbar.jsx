import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { logoutUser } from './auth';

const Navbar = () => {
    const navigate = useNavigate();
    const isLoggedIn = !!localStorage.getItem('access');

    const handleLogout = () => {
        const confirmLogout = window.confirm('Are you sure you want to log out?');
        if (confirmLogout) {
            logoutUser();
            localStorage.clear(); // Clear all session data
            navigate('/login');
        }
    };

    return (
        <nav className="bg-gray-800 text-white p-4 flex gap-4">
            <Link to="/">Home</Link>
            {!isLoggedIn ? (
                <>
                    <Link to="/register">Register</Link>
                    <Link to="/login">Login</Link>
                </>
            ) : (
                <>
                    <Link to="/profile">Profile</Link>
                    <button
                        onClick={handleLogout}
                        className="ml-auto text-red-400 hover:text-red-600 transition duration-300"
                    >
                        Logout
                    </button>
                </>
            )}
        </nav>
    );
};

export default Navbar;