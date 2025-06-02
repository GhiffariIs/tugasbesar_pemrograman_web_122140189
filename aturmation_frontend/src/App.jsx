import React, { useEffect, useState } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Box, CssBaseline, ThemeProvider } from '@mui/material';
import { theme } from './theme';

// Layouts
import MainLayout from './components/layout/MainLayout';

// Pages
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import HomePage from './pages/HomePage';
import ProductsPage from './pages/ProductsPage';
import ProductDetailPage from './pages/ProductDetailPage';
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

  // Proteksi route
  const ProtectedRoute = ({ children, roles }) => {
    if (loading) return <div>Loading...</div>;
    
    if (!user) {
      return <Navigate to="/login" replace />;
    }
    
    if (roles && !roles.includes(user.role)) {
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
                <HomePage />
              </MainLayout>
            </ProtectedRoute>
          } />
          
          {/* Product Routes */}
          <Route path="/products" element={
            <ProtectedRoute roles={['admin', 'staff']}>
              <MainLayout user={user} setUser={setUser}>
                <ProductsPage />
              </MainLayout>
            </ProtectedRoute>
          } />
          
          <Route path="/products/:id" element={
            <ProtectedRoute roles={['admin', 'staff']}>
              <MainLayout user={user} setUser={setUser}>
                <ProductDetailPage />
              </MainLayout>
            </ProtectedRoute>
          } />
          
          {/* User Management - admin only */}
          <Route path="/users" element={
            <ProtectedRoute roles={['admin']}>
              <MainLayout user={user} setUser={setUser}>
                <UsersPage />
              </MainLayout>
            </ProtectedRoute>
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
