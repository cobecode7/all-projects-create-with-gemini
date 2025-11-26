import React, { useState, useEffect, useContext } from 'react';
import { useParams } from 'react-router-dom';
import api from '../services/api';
import { AuthContext } from '../context/AuthContext';

const OrderDetail = () => {
  const { id } = useParams();
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { user } = useContext(AuthContext);

  useEffect(() => {
    const fetchOrder = async () => {
      try {
        const response = await api.get(`/orders/${id}`);
        setOrder(response.data);
        setLoading(false);
      } catch (error) {
        setError(error.message);
        setLoading(false);
      }
    };

    if (user) {
      fetchOrder();
    }
  }, [user, id]);

  if (loading) {
    return <div className="container text-center mt-5">Loading...</div>;
  }

  if (error) {
    return <div className="container text-center mt-5">Error: {error}</div>;
  }

  if (!order) {
    return <div className="container text-center mt-5">Order not found.</div>;
  }

  return (
    <div className="container my-5">
      <div className="card shadow-sm">
        <div className="card-body">
          <h2 className="card-title">Order Details</h2>
          <div className="row">
            <div className="col-md-6">
              <p><strong>Order ID:</strong> {order.id}</p>
              <p><strong>Order Date:</strong> {new Date(order.created_at).toLocaleDateString()}</p>
              <p><strong>Total:</strong> ${order.total.toFixed(2)}</p>
              <p><strong>Status:</strong> <span className={`badge bg-${order.status === 'delivered' ? 'success' : 'warning'}`}>{order.status}</span></p>
            </div>
            <div className="col-md-6">
              <p><strong>Shipping Address:</strong> {order.shipping_address}</p>
              <p><strong>Payment Method:</strong> {order.payment_method}</p>
            </div>
          </div>
        </div>
      </div>

      <h3 className="mt-4">Order Items</h3>
      <div className="card shadow-sm">
        <div className="card-body">
          <table className="table table-hover">
            <thead>
              <tr>
                <th>Product</th>
                <th>Price</th>
                <th>Quantity</th>
                <th>Total</th>
              </tr>
            </thead>
            <tbody>
              {order.order_items.map((item) => (
                <tr key={item.id}>
                  <td>{item.product.name}</td>
                  <td>${item.price.toFixed(2)}</td>
                  <td>{item.quantity}</td>
                  <td>${(item.price * item.quantity).toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default OrderDetail;
