import React, { useEffect, useState } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Box, CssBaseline, ThemeProvider, CircularProgress } from '@mui/material';
import { theme } from './theme';

// Layouts
import MainLayout from './components/layout/MainLayout';

// Pages
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import HomePage from './pages/HomePage';
import ProductsPage from './pages/ProductsPage';
import ProductDetailPage from './pages/ProductDetailPage';
import AddProductPage from './pages/AddProductPage';
import EditProductPage from './pages/EditProductPage';
import UsersPage from './pages/UsersPage';
import SettingsPage from './pages/SettingsPage';
import NotFoundPage from './pages/NotFoundPage';

// Services
import { authService } from './services/services';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const userData = await authService.getCurrentUser();
        setUser(userData);
      } catch (error) {
        console.error('Error fetching user:', error);
        // Clear token if authentication fails
        localStorage.removeItem('token');
      } finally {
        setLoading(false);
      }
    };

    if (localStorage.getItem('token')) {
      fetchUser();
    } else {
      setLoading(false);
    }
  }, []);

  if (loading) {
    return (
      <Box 
        sx={{ 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center', 
          height: '100vh' 
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  // Proteksi route
  const ProtectedRoute = ({ children }) => {
    if (!user) {
      return <Navigate to="/login" replace />;
    }
    return children;
  };

  // Admin route protection
  const AdminRoute = ({ children }) => {
    if (!user) {
      return <Navigate to="/login" replace />;
    }
    
    if (user.role !== 'admin') {
      return <Navigate to="/" replace />;
    }
    
    return children;
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: 'flex', minHeight: '100vh' }}>
        <Routes>
          {/* Auth Routes */}
          <Route path="/login" element={user ? <Navigate to="/" replace /> : <LoginPage setUser={setUser} />} />
          <Route path="/register" element={user ? <Navigate to="/" replace /> : <RegisterPage setUser={setUser} />} />
          
          {/* Main Routes */}
          <Route path="/" element={
            <ProtectedRoute>
              <MainLayout user={user} setUser={setUser}>
                <HomePage user={user} />
              </MainLayout>
            </ProtectedRoute>
          } />
          
          {/* Product Routes */}
          <Route path="/products" element={
            <ProtectedRoute>
              <MainLayout user={user} setUser={setUser}>
                <ProductsPage />
              </MainLayout>
            </ProtectedRoute>
          } />
          
          <Route path="/products/create" element={
            <ProtectedRoute>
              <MainLayout user={user} setUser={setUser}>
                <AddProductPage />
              </MainLayout>
            </ProtectedRoute>
          } />
          
          <Route path="/products/:id" element={
            <ProtectedRoute>
              <MainLayout user={user} setUser={setUser}>
                <ProductDetailPage />
              </MainLayout>
            </ProtectedRoute>
          } />
          
          <Route path="/products/:id/edit" element={
            <ProtectedRoute>
              <MainLayout user={user} setUser={setUser}>
                <EditProductPage />
              </MainLayout>
            </ProtectedRoute>
          } />
          
          {/* User Management - admin only */}
          <Route path="/users" element={
            <AdminRoute>
              <MainLayout user={user} setUser={setUser}>
                <UsersPage />
              </MainLayout>
            </AdminRoute>
          } />
          
          {/* Settings */}
          <Route path="/settings" element={
            <ProtectedRoute>
              <MainLayout user={user} setUser={setUser}>
                <SettingsPage user={user} />
              </MainLayout>
            </ProtectedRoute>
          } />
          
          {/* 404 Page */}
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </Box>
    </ThemeProvider>
  );
}

export default App;
