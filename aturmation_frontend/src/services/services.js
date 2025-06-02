import axios from 'axios';

// Mendapatkan API URL dari variabel lingkungan atau gunakan default
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:6543/api/v1';

// Interceptor untuk menambahkan token ke setiap request
const authAxios = axios.create({
  baseURL: API_URL,
});

authAxios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Auth Service
export const authService = {
  login: async (username, password) => {
    try {
      const response = await axios.post(`${API_URL}/auth/login`, { username, password });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  register: async (userData) => {
    try {
      const response = await axios.post(`${API_URL}/auth/register`, userData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getCurrentUser: async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) return null;
      
      const response = await authAxios.get(`${API_URL}/auth/me`);
      return response.data;
    } catch (error) {
      console.error('Failed to get current user:', error);
      localStorage.removeItem('token');
      return null;
    }
  },

  logout: async () => {
    try {
      localStorage.removeItem('token');
      return true;
    } catch (error) {
      throw error;
    }
  },
};

// Product Service
export const productService = {
  getAllProducts: async (params) => {
    try {
      const response = await authAxios.get(`${API_URL}/products`, { params });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getProductById: async (id) => {
    try {
      const response = await authAxios.get(`${API_URL}/products/${id}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  createProduct: async (productData) => {
    try {
      // Pastikan sku disertakan, backend mungkin membutuhkannya
      const formattedData = {
        name: String(productData.name).trim(),
        price: Number(productData.price),
        stock: Number(productData.stock),
        minStock: Number(productData.minStock || 10),
        // Generate temporary SKU, backend akan menggantinya dengan ID
        sku: `TEMP-${Date.now()}`, // Nilai sementara yang akan diganti backend
        ...(productData.description ? { description: String(productData.description).trim() } : {})
      };
      
      console.log('Data formatted for API:', formattedData);
      
      const response = await authAxios.post(`${API_URL}/products`, formattedData);
      return response.data;
    } catch (error) {
      console.error('Service error creating product:', error);
      throw error;
    }
  },

  updateProduct: async (id, productData) => {
    try {
      // Pastikan SKU tidak dikirim dalam update
      const { sku, ...dataWithoutSku } = productData;
      
      const response = await authAxios.put(`${API_URL}/products/${id}`, dataWithoutSku);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  deleteProduct: async (id) => {
    try {
      const response = await authAxios.delete(`${API_URL}/products/${id}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};

// User Service
export const userService = {
  getAllUsers: async () => {
    try {
      const response = await authAxios.get(`${API_URL}/users`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getUserById: async (id) => {
    try {
      const response = await authAxios.get(`${API_URL}/users/${id}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  createUser: async (userData) => {
    try {
      const response = await authAxios.post(`${API_URL}/users`, userData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  updateUser: async (id, userData) => {
    try {
      const response = await authAxios.put(`${API_URL}/users/${id}`, userData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  deleteUser: async (id) => {
    try {
      const response = await authAxios.delete(`${API_URL}/users/${id}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};
