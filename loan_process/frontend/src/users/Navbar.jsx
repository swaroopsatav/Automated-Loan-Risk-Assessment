import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { logoutUser } from './auth';

const Navbar = () => {
    const navigate = useNavigate();
    const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('access'));

    // Update the login state when the access token changes
    useEffect(() => {
        const handleStorageChange = () => {
            setIsLoggedIn(!!localStorage.getItem('access'));
        };

        window.addEventListener('storage', handleStorageChange);
        return () => {
            window.removeEventListener('storage', handleStorageChange);
        };
    }, []);

    // Handle user logout
    const handleLogout = () => {
        const confirmLogout = window.confirm('Are you sure you want to log out?');
        if (confirmLogout) {
            try {
                logoutUser(); // Clear tokens
                setIsLoggedIn(false); // Update the login state
                navigate('/login'); // Redirect to login page
            } catch (error) {
                console.error('Failed to log out:', error);
                alert('Something went wrong while logging out. Please try again.');
            }
        }
    };

    return (
        <nav className="bg-gray-800 text-white p-4 flex items-center gap-4">
            <Link to="/" className="hover:text-blue-300 transition duration-300">
                Home
            </Link>
            {!isLoggedIn ? (
                <>
                    <Link
                        to="/register"
                        className="hover:text-blue-300 transition duration-300"
                    >
                        Register
                    </Link>
                    <Link
                        to="/login"
                        className="hover:text-blue-300 transition duration-300"
                    >
                        Login
                    </Link>
                </>
            ) : (
                <>
                    <Link
                        to="/profile"
                        className="hover:text-blue-300 transition duration-300"
                    >
                        Profile
                    </Link>
                    <button
                        onClick={handleLogout}
                        className="ml-auto text-red-400 hover:text-red-600 transition duration-300"
                        aria-label="Logout"
                    >
                        Logout
                    </button>
                </>
            )}
        </nav>
    );
};

export default Navbar;