import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { logoutUser } from './auth';

const Navbar = () => {
  const navigate = useNavigate();
  const isLoggedIn = !!localStorage.getItem('access');

  const handleLogout = () => {
    logoutUser();
    navigate('/login');
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
          <button onClick={handleLogout} className="ml-auto text-red-400">Logout</button>
        </>
      )}
    </nav>
  );
};

export default Navbar;
