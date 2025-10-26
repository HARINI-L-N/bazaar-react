import axios from 'axios';

// Configure base URL for your Flask backend
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for authentication
api.interceptors.request.use(
  (config) => {
    const user = localStorage.getItem('user');
    if (user) {
      const { token } = JSON.parse(user);
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// API endpoints
export const endpoints = {
  // Products
  getProducts: () => api.get('/products'),
  getProduct: (id: string) => api.get(`/products/${id}`),
  getRecommendations: (userId: string) => api.get(`/recommendations/${userId}`),
  // Product-level content recommendations (no auth required)
  getProductRecommendations: (productId: string) => api.get(`/recommendations/content/${productId}`),
  getCategories: () => api.get('/products/categories'),
  getFeaturedProducts: () => api.get('/products/featured'),
  
  // Users
  register: (data: { username: string; email: string; password: string; first_name?: string; last_name?: string }) =>
    api.post('/users/register', data),
  login: (data: { username: string; password: string }) =>
    api.post('/users/login', data),
  getProfile: () => api.get('/users/profile'),
  updateProfile: (data: any) => api.put('/users/profile', data),
  getUserHistory: (userId: string) => api.get(`/users/${userId}/history`),
  getUserOrders: (userId: string) => api.get(`/users/${userId}/orders`),
  
  // Cart
  getCart: () => api.get('/cart'),
  addToCart: (data: { product_id: string; quantity: number }) =>
    api.post('/cart', data),
  updateCartItem: (productId: string, quantity: number) =>
    api.put(`/cart/${productId}`, { quantity }),
  removeFromCart: (productId: string) => api.delete(`/cart/${productId}`),
  clearCart: () => api.delete('/cart/clear'),
  
  // Orders
  getOrders: () => api.get('/orders'),
  getOrder: (orderId: string) => api.get(`/orders/${orderId}`),
  createOrder: (data: { shipping_address: any; payment_method: string }) =>
    api.post('/orders', data),
  updateOrderStatus: (orderId: string, status: string) =>
    api.put(`/orders/${orderId}/status`, { status }),
  
  // Tracking
  trackProductView: (data: { product_id: string; view_duration?: number }) =>
    api.post('/track/view', data),
  getRecentHistory: (userId: string) => api.get(`/users/${userId}/history/recent`),
};

export default api;
