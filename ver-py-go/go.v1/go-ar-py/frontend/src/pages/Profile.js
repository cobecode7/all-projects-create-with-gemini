import React, { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

const Profile = () => {
  const { user } = useContext(AuthContext);

  if (!user) {
    return <div className="container text-center mt-5">Loading...</div>;
  }

  return (
    <div className="container my-5">
      <div className="row justify-content-center">
        <div className="col-md-8">
          <div className="card shadow-sm">
            <div className="card-body">
              <h2 className="card-title text-center mb-4">Profile</h2>
              <div className="row">
                <div className="col-md-4 text-center">
                  <img src="https://via.placeholder.com/150" className="img-fluid rounded-circle" alt="profile" />
                </div>
                <div className="col-md-8">
                  <p><strong>First Name:</strong> {user.first_name}</p>
                  <p><strong>Last Name:</strong> {user.last_name}</p>
                  <p><strong>Email:</strong> {user.email}</p>
                  <p><strong>Role:</strong> {user.role}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
