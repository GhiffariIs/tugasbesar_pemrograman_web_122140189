import axios from 'axios'

// Create axios instance with default config
const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add token to requests if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// API endpoints
export const authApi = {
  login: (data) => api.post('/auth/login', data),
  register: (data) => api.post('/auth/register', data),
  getProfile: () => api.get('/auth/me')
}

export const productsApi = {
  getAll: () => api.get('/products'),
  getById: (id) => api.get(`/products/${id}`),
  create: (data) => api.post('/products', data),
  update: (id, data) => api.put(`/products/${id}`, data),
  delete: (id) => api.delete(`/products/${id}`)
}

export const categoriesApi = {
  getAll: () => api.get('/categories'),
  getById: (id) => api.get(`/categories/${id}`),
  create: (data) => api.post('/categories', data),
  update: (id, data) => api.put(`/categories/${id}`, data),
  delete: (id) => api.delete(`/categories/${id}`)
}

export const inventoryApi = {
  updateStock: (id, quantity) => api.patch(`/products/${id}/stock`, { quantity }),
  getLowStock: () => api.get('/products/low-stock'),
  getStockHistory: (id) => api.get(`/products/${id}/stock-history`)
}

export const usersApi = {
  getAll: () => api.get('/users'),
  getById: (id) => api.get(`/users/${id}`),
  create: (data) => api.post('/users', data),
  update: (id, data) => api.put(`/users/${id}`, data),
  delete: (id) => api.delete(`/users/${id}`),
  updateStatus: (id, isActive) => api.patch(`/users/${id}/status`, { isActive })
}

export const stockApi = {
  getStockLevels: () => api.get('/inventory/stock-levels'),
  updateStock: (productId, quantity, type = 'set') => 
    api.patch(`/inventory/stock/${productId}`, { quantity, type }),
  getLowStock: (threshold) => api.get('/inventory/low-stock', { params: { threshold }}),
  getStockHistory: (productId, timeRange) => 
    api.get(`/inventory/stock-history/${productId}`, { params: { timeRange }}),
  getStockReport: (timeRange = 'week') => 
    api.get('/inventory/report', { params: { timeRange }})
}

// Error handling
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error.response?.data || error.message)
  }
)

export default api