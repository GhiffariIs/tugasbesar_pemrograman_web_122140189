import axios from 'axios';

// Ubah BASE_URL sesuai dengan endpoint backend Pyramid
const BASE_URL = 'http://localhost:6543/api/v1';

// Create axios instance with base URL and CORS configuration
const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  },
  // Penting: Tambahkan withCredentials untuk CORS dengan kredensial
  withCredentials: false
});

// Add request interceptor to include auth token in requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add response interceptor to handle common error scenarios
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle CORS errors khusus
    if (error.message === 'Network Error') {
      console.error('CORS or network error occurred. Check if the backend is running and CORS is configured correctly.');
    }
    
    // Handle 401 Unauthorized errors
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      window.location = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
