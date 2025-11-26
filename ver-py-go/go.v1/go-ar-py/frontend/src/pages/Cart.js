import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { CartContext } from '../context/CartContext';

const Cart = () => {
  const { cart, updateCartItem, removeFromCart, clearCart } = useContext(CartContext);

  const getTotal = () => {
    return cart.cart_items.reduce((total, item) => total + item.product.price * item.quantity, 0).toFixed(2);
  };

  if (!cart || !cart.cart_items || cart.cart_items.length === 0) {
    return (
      <div className="container text-center my-5">
        <h2>Your cart is empty.</h2>
        <Link to="/products" className="btn btn-primary mt-3">Continue Shopping</Link>
      </div>
    );
  }

  return (
    <div className="container my-5">
      <h2>Your Cart</h2>
      <div className="card shadow-sm">
        <div className="card-body">
          <table className="table table-hover">
            <thead>
              <tr>
                <th>Product</th>
                <th>Price</th>
                <th>Quantity</th>
                <th>Total</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {cart.cart_items.map((item) => (
                <tr key={item.id}>
                  <td>{item.product.name}</td>
                  <td>${item.product.price}</td>
                  <td>
                    <input
                      type="number"
                      className="form-control w-50"
                      value={item.quantity}
                      onChange={(e) => updateCartItem(item.id, parseInt(e.target.value))}
                      min="1"
                    />
                  </td>
                  <td>${(item.product.price * item.quantity).toFixed(2)}</td>
                  <td>
                    <button className="btn btn-danger btn-sm" onClick={() => removeFromCart(item.id)}>Remove</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      <div className="d-flex justify-content-between align-items-center mt-4">
        <button className="btn btn-outline-danger" onClick={clearCart}>Clear Cart</button>
        <div className="text-end">
          <h4>Total: ${getTotal()}</h4>
          <Link to="/orders" className="btn btn-primary">Checkout</Link>
        </div>
      </div>
    </div>
  );
};

export default Cart;
