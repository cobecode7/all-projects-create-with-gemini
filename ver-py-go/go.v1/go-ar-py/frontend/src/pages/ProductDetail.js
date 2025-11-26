import React, { useState, useEffect, useContext } from 'react';
import { useParams } from 'react-router-dom';
import api from '../services/api';
import { CartContext } from '../context/CartContext';

const ProductDetail = () => {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { addToCart } = useContext(CartContext);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const response = await api.get(`/products/${id}`);
        setProduct(response.data);
        setLoading(false);
      } catch (error) {
        setError(error.message);
        setLoading(false);
      }
    };

    fetchProduct();
  }, [id]);

  if (loading) {
    return <div className="container text-center mt-5">Loading...</div>;
  }

  if (error) {
    return <div className="container text-center mt-5">Error: {error}</div>;
  }

  return (
    <div className="container my-5">
      <div className="row">
        <div className="col-md-6">
          <img src={product.image_url || 'https://via.placeholder.com/500x500'} className="img-fluid rounded" alt={product.name} />
        </div>
        <div className="col-md-6">
          <h1 className="display-5 fw-bold">{product.name}</h1>
          <p className="lead">{product.description}</p>
          <hr />
          <h3 className="fw-bold">${product.price}</h3>
          <p>Stock: {product.stock}</p>
          <div className="d-grid gap-2 col-6">
            <button className="btn btn-primary btn-lg" onClick={() => addToCart(product, 1)}>Add to Cart</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductDetail;
