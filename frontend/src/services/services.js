import api from './api';

// Mock data untuk login testing tanpa backend
const mockUsers = [
  {
    id: 1,
    username: 'admin',
    password: 'admin123',
    name: 'Administrator',
    email: 'admin@aturmation.com',
    role: 'admin'
  },
  {
    id: 2,
    username: 'staff',
    password: 'staff123',
    name: 'Staff Demo',
    email: 'staff@aturmation.com',
    role: 'staff'
  }
];

export const authService = {
  login: async (username, password) => {
    // Cek apakah backend sudah berjalan
    try {
      // Coba koneksi ke backend dulu
      const response = await api.post('/auth/login', { username, password });
      return response.data;
    } catch (error) {
      // Jika backend belum tersedia, gunakan mock login
      console.log('Backend not available, using mock login');
      
      // Mencari user yang cocok
      const user = mockUsers.find(u => 
        u.username === username && u.password === password
      );
      
      if (!user) {
        // Simulasi error response dari server
        const mockError = new Error('Invalid username or password');
        mockError.response = {
          data: {
            message: 'Username atau password tidak valid'
          }
        };
        throw mockError;
      }
      
      // Hapus password dari objek user untuk keamanan
      const { password: _, ...userWithoutPassword } = user;
      
      // Membuat JWT token palsu untuk demo
      const mockToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJhZG1pbiIsIm5hbWUiOiJBZG1pbmlzdHJhdG9yIiwiZW1haWwiOiJhZG1pbkBhdHVybWF0aW9uLmNvbSIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcwODgyNjUwOX0.fake-signature';
      
      // Simulasi delay network
      await new Promise(resolve => setTimeout(resolve, 500));
      
      return {
        token: mockToken,
        user: userWithoutPassword
      };
    }
  },
  
  register: async (userData) => {
    try {
      const response = await api.post('/auth/register', userData);
      return response.data;
    } catch (error) {
      // Mock register jika backend belum tersedia
      console.log('Backend not available, using mock register');
      
      // Cek apakah username sudah ada
      if (mockUsers.some(u => u.username === userData.username)) {
        const mockError = new Error('Username already exists');
        mockError.response = {
          data: {
            message: 'Username sudah digunakan'
          }
        };
        throw mockError;
      }
      
      // Cek apakah email sudah ada
      if (mockUsers.some(u => u.email === userData.email)) {
        const mockError = new Error('Email already exists');
        mockError.response = {
          data: {
            message: 'Email sudah digunakan'
          }
        };
        throw mockError;
      }
      
      // Membuat JWT token palsu untuk demo
      const mockToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MywidXNlcm5hbWUiOiJuZXd1c2VyIiwibmFtZSI6Ik5ldyBVc2VyIiwiZW1haWwiOiJuZXdAdXNlci5jb20iLCJyb2xlIjoic3RhZmYiLCJleHAiOjE3MDg4MjY1MDl9.fake-signature';
      
      // Simulasi delay network
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const newUser = {
        id: 3,
        ...userData,
        role: 'staff'
      };
      
      const { password: _, ...userWithoutPassword } = newUser;
      
      return {
        token: mockToken,
        user: userWithoutPassword
      };
    }
  },
  
  getCurrentUser: async () => {
    try {
      const response = await api.get('/auth/me');
      return response.data;
    } catch (error) {
      console.log('Backend not available, using mock user data');
      
      // Ambil token dari localStorage
      const token = localStorage.getItem('token');
      
      // Jika tidak ada token, return null
      if (!token) {
        return null;
      }
      
      // Untuk demo, selalu return user admin
      return {
        id: 1,
        username: 'admin',
        name: 'Administrator',
        email: 'admin@aturmation.com',
        role: 'admin'
      };
    }
  }
};

export const categoryService = {
  getAllCategories: async () => {
    const response = await api.get('/categories');
    return response.data;
  },
  
  getCategoryById: async (id) => {
    const response = await api.get(`/categories/${id}`);
    return response.data;
  },
  
  createCategory: async (categoryData) => {
    const response = await api.post('/categories', categoryData);
    return response.data;
  },
  
  updateCategory: async (id, categoryData) => {
    const response = await api.put(`/categories/${id}`, categoryData);
    return response.data;
  },
  
  deleteCategory: async (id) => {
    const response = await api.delete(`/categories/${id}`);
    return response.data;
  }
};

export const productService = {
  getAllProducts: async (params) => {
    const response = await api.get('/products', { params });
    return response.data;
  },
  
  getProductById: async (id) => {
    const response = await api.get(`/products/${id}`);
    return response.data;
  },
  
  createProduct: async (productData) => {
    const response = await api.post('/products', productData);
    return response.data;
  },
  
  updateProduct: async (id, productData) => {
    const response = await api.put(`/products/${id}`, productData);
    return response.data;
  },
  
  deleteProduct: async (id) => {
    const response = await api.delete(`/products/${id}`);
    return response.data;
  },
  
  searchProducts: async (query) => {
    const response = await api.get(`/products/search?q=${query}`);
    return response.data;
  },
  
  getLowStockProducts: async () => {
    const response = await api.get('/products/low-stock');
    return response.data;
  }
};

export const transactionService = {
  getAllTransactions: async (params) => {
    const response = await api.get('/transactions', { params });
    return response.data;
  },
  
  getTransactionById: async (id) => {
    const response = await api.get(`/transactions/${id}`);
    return response.data;
  },
  
  createTransaction: async (transactionData) => {
    const response = await api.post('/transactions', transactionData);
    return response.data;
  },
  
  getStockInTransactions: async (params) => {
    const response = await api.get('/transactions/stock-in', { params });
    return response.data;
  },
  
  getStockOutTransactions: async (params) => {
    const response = await api.get('/transactions/stock-out', { params });
    return response.data;
  }
};

export const reportService = {
  getStockReport: async (params) => {
    const response = await api.get('/reports/stock', { params });
    return response.data;
  },
  
  getTransactionReport: async (params) => {
    const response = await api.get('/reports/transactions', { params });
    return response.data;
  },
  
  getProductMovementReport: async (productId, params) => {
    const response = await api.get(`/reports/product-movement/${productId}`, { params });
    return response.data;
  }
};
