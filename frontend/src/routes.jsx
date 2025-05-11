import { Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/layout/Layout'
import LoginPage from './pages/auth/LoginPage'
import RegisterPage from './pages/auth/RegisterPage'
import DashboardPage from './pages/dashboard/DashboardPage'
import ProductsPage from './pages/products/ProductsPage'
import InventoryPage from './pages/inventory/InventoryPage'
import CategoryPage from './pages/categories/CategoryPage'
import TransactionsPage from './pages/transactions/TransactionsPage'
import ReportsPage from './pages/reports/ReportsPage'
import UsersPage from './pages/users/UsersPage'
import SettingsPage from './pages/settings/SettingsPage'
import { useAuth } from './hooks/useAuth'

const PrivateRoute = ({ children, requireAdmin }) => {
  const { user, loading } = useAuth()
  
  if (loading) {
    return null // or loading spinner
  }
  
  if (!user) {
    return <Navigate to="/login" />
  }

  if (requireAdmin && user.role !== 'admin') {
    return <Navigate to="/" />
  }
  
  return children
}

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      
      <Route path="/" element={
        <PrivateRoute>
          <Layout />
        </PrivateRoute>
      }>
        <Route index element={<DashboardPage />} />
        <Route path="products" element={<ProductsPage />} />
        <Route path="categories" element={<CategoryPage />} />
        <Route path="inventory" element={<InventoryPage />} />
        <Route path="transactions" element={<TransactionsPage />} />
        
        {/* Admin only routes */}
        <Route path="reports" element={
          <PrivateRoute requireAdmin>
            <ReportsPage />
          </PrivateRoute>
        } />
        <Route path="users" element={
          <PrivateRoute requireAdmin>
            <UsersPage />
          </PrivateRoute>
        } />
        <Route path="settings" element={
          <PrivateRoute requireAdmin>
            <SettingsPage />
          </PrivateRoute>
        } />
      </Route>

      {/* Catch all route */}
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  )
}

export default AppRoutes