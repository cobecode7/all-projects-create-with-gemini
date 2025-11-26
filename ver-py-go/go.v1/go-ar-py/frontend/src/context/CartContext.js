import React, { createContext, useState, useEffect, useContext } from 'react';
import api from '../services/api';
import { AuthContext } from './AuthContext';

export const CartContext = createContext();

export const CartProvider = ({ children }) => {
  const [cart, setCart] = useState(null);
  const [cartCount, setCartCount] = useState(0);
  const [loading, setLoading] = useState(false);
  const { isAuthenticated } = useContext(AuthContext);

  useEffect(() => {
    if (isAuthenticated) {
      fetchCart();
    } else {
      setCart(null);
      setCartCount(0);
    }
  }, [isAuthenticated]);

  const fetchCart = async () => {
    try {
      setLoading(true);
      const response = await api.get('/api/v1/cart');
      setCart(response.data);

      // حساب عدد العناصر في عربة التسوق
      const count = response.data.cart_items?.reduce((total, item) => total + item.quantity, 0) || 0;
      setCartCount(count);
    } catch (error) {
      console.error('Error fetching cart:', error);
    } finally {
      setLoading(false);
    }
  };

  const addToCart = async (productId, quantity) => {
    try {
      setLoading(true);
      await api.post('/api/v1/cart', { product_id: productId, quantity });
      await fetchCart();
      return { success: true };
    } catch (error) {
      console.error('Error adding to cart:', error);
      return { 
        success: false, 
        message: error.response?.data?.message || 'فشل إضافة المنتج إلى عربة التسوق' 
      };
    } finally {
      setLoading(false);
    }
  };

  const updateCartItem = async (itemId, quantity) => {
    try {
      setLoading(true);
      await api.put(`/api/v1/cart?id=${itemId}`, { quantity });
      await fetchCart();
      return { success: true };
    } catch (error) {
      console.error('Error updating cart item:', error);
      return { 
        success: false, 
        message: error.response?.data?.message || 'فشل تحديث كمية المنتج' 
      };
    } finally {
      setLoading(false);
    }
  };

  const removeFromCart = async (itemId) => {
    try {
      setLoading(true);
      await api.delete(`/api/v1/cart?id=${itemId}`);
      await fetchCart();
      return { success: true };
    } catch (error) {
      console.error('Error removing from cart:', error);
      return { 
        success: false, 
        message: error.response?.data?.message || 'فشل إزالة المنتج من عربة التسوق' 
      };
    } finally {
      setLoading(false);
    }
  };

  const clearCart = async () => {
    try {
      setLoading(true);
      await api.delete('/api/v1/cart/clear');
      await fetchCart();
      return { success: true };
    } catch (error) {
      console.error('Error clearing cart:', error);
      return { 
        success: false, 
        message: error.response?.data?.message || 'فشل تفريغ عربة التسوق' 
      };
    } finally {
      setLoading(false);
    }
  };

  return (
    <CartContext.Provider value={{
      cart,
      cartCount,
      loading,
      fetchCart,
      addToCart,
      updateCartItem,
      removeFromCart,
      clearCart
    }}>
      {children}
    </CartContext.Provider>
  );
};