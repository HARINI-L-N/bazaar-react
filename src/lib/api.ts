import axios from 'axios';

// Configure base URL for your Flask backend
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';

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
  getRecommendations: (id: string) => api.get(`/recommendations/${id}`),
  
  // Users
  register: (data: { email: string; password: string; name: string }) =>
    api.post('/users/register', data),
  login: (data: { email: string; password: string }) =>
    api.post('/users/login', data),
  getUserHistory: (userId: string) => api.get(`/users/${userId}/history`),
  getUserOrders: (userId: string) => api.get(`/users/${userId}/orders`),
  
  // Cart
  getCart: () => api.get('/cart'),
  addToCart: (data: { productId: string; quantity: number }) =>
    api.post('/cart', data),
  updateCart: (itemId: string, quantity: number) =>
    api.put(`/cart/${itemId}`, { quantity }),
  removeFromCart: (itemId: string) => api.delete(`/cart/${itemId}`),
  
  // Orders
  getOrders: () => api.get('/orders'),
  createOrder: (data: { items: any[]; total: number }) =>
    api.post('/orders', data),
};

export default api;
