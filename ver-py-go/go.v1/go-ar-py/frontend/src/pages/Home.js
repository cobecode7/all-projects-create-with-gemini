import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="container my-5">
      <div className="row p-4 pb-0 pe-lg-0 pt-lg-5 align-items-center rounded-3 border shadow-lg">
        <div className="col-lg-7 p-3 p-lg-5 pt-lg-3">
          <h1 className="display-4 fw-bold lh-1">Welcome to our E-commerce Store</h1>
          <p className="lead">We have a wide range of products for you to choose from. Find the best products at the best prices.</p>
          <div className="d-grid gap-2 d-md-flex justify-content-md-start mb-4 mb-lg-3">
            <Link to="/products" className="btn btn-primary btn-lg px-4 me-md-2 fw-bold">Browse Products</Link>
            <Link to="/register" className="btn btn-outline-secondary btn-lg px-4">Register</Link>
          </div>
        </div>
        <div className="col-lg-4 offset-lg-1 p-0 overflow-hidden shadow-lg">
            <img className="rounded-lg-3" src="https://via.placeholder.com/720x600" alt="" width="720" />
        </div>
      </div>
    </div>
  );
};

export default Home;
