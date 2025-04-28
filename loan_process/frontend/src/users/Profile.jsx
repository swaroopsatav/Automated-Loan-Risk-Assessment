import React, { useEffect, useState } from 'react';
import API from './api';

const Profile = () => {
  const [profile, setProfile] = useState(null);
  const [isLoading, setIsLoading] = useState(true); // Loading state
  const [error, setError] = useState(''); // Error state

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await API.get('api/profile/');
        setProfile(res.data);
      } catch (err) {
        console.error('Error fetching profile:', err);
        setError('Failed to load profile. Please try again later.');
      } finally {
        setIsLoading(false); // Stop loading once request is done
      }
    };

    fetchProfile();
  }, []);

  if (isLoading) {
    return <p className="text-center">Loading...</p>; // Display a loading message
  }

  if (error) {
    return <p className="text-center text-red-600">{error}</p>; // Display an error message
  }

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h2 className="text-xl font-bold">My Profile</h2>
      {profile ? (
        <form className="mt-4 space-y-2">
          <div>
            <label className="block font-bold">Username:</label>
            <input
              type="text"
              value={profile.username}
              readOnly
              className="w-full border p-2 rounded"
            />
          </div>
          <div>
            <label className="block font-bold">Email:</label>
            <input
              type="email"
              value={profile.email}
              readOnly
              className="w-full border p-2 rounded"
            />
          </div>
          <div>
            <label className="block font-bold">Phone:</label>
            <input
              type="text"
              value={profile.phone_number}
              readOnly
              className="w-full border p-2 rounded"
            />
          </div>
          <div>
            <label className="block font-bold">KYC Verified:</label>
            <input
              type="text"
              value={profile.is_kyc_verified ? '✅' : '❌'}
              readOnly
              className="w-full border p-2 rounded"
            />
          </div>
          <div>
            <label className="block font-bold">Credit Score:</label>
            <input
              type="text"
              value={profile.credit_score ?? 'N/A'}
              readOnly
              className="w-full border p-2 rounded"
            />
          </div>
          <div>
            <label className="block font-bold">Experian Sync:</label>
            <input
              type="text"
              value={profile.last_experian_sync ?? 'N/A'}
              readOnly
              className="w-full border p-2 rounded"
            />
          </div>
        </form>
      ) : (
        <p className="text-center">No profile data available.</p>
      )}
    </div>
  );
};

export default Profile;