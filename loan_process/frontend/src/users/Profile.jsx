import React, {useEffect, useState} from 'react';
import API from './api';

const Profile = () => {
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    API.get('api/profile/')
        .then(res => setProfile(res.data))
        .catch(err => console.error(err));
  }, []);

  return (
      <div className="p-4 max-w-xl mx-auto">
        <h2 className="text-xl font-bold">My Profile</h2>
        {profile ? (
            <form className="mt-4 space-y-2">
              <div>
                <label className="block font-bold">Username:</label>
                <input type="text" value={profile.username} readOnly className="w-full border p-2 rounded"/>
              </div>
              <div>
                <label className="block font-bold">Email:</label>
                <input type="email" value={profile.email} readOnly className="w-full border p-2 rounded"/>
              </div>
              <div>
                <label className="block font-bold">Phone:</label>
                <input type="text" value={profile.phone_number} readOnly className="w-full border p-2 rounded"/>
              </div>
              <div>
                <label className="block font-bold">KYC Verified:</label>
                <input type="text" value={profile.is_kyc_verified ? '✅' : '❌'} readOnly
                       className="w-full border p-2 rounded"/>
              </div>
              <div>
                <label className="block font-bold">Credit Score:</label>
                <input type="text" value={profile.credit_score ?? 'N/A'} readOnly
                       className="w-full border p-2 rounded"/>
              </div>
              <div>
                <label className="block font-bold">Experian Sync:</label>
                <input type="text" value={profile.last_experian_sync ?? 'N/A'} readOnly
                       className="w-full border p-2 rounded"/>
              </div>
            </form>
        ) : <p>Loading...</p>}
      </div>
  );
};

export default Profile;
