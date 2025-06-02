import api from '../services/api';
import { authService, productService } from '../services/services';

// Fungsi untuk menguji koneksi dasar
export const testConnection = async () => {
  try {
    // Ping backend untuk memastikan hidup
    await api.get('/auth/me');
    console.log('✅ Backend connection successful');
    return true;
  } catch (error) {
    if (error.response) {
      // Jika ada response, backend hidup meski error (e.g., 401 Unauthorized)
      console.log('✅ Backend connection successful (received error response)');
      return true;
    }
    console.error('❌ Backend connection failed:', error.message);
    return false;
  }
};

// Test auth flow
export const testAuthFlow = async () => {
  try {
    // 1. Login
    console.log('Testing login...');
    const loginResult = await authService.login('admin', 'adminpassword');
    console.log('✅ Login successful:', loginResult);
    
    // 2. Get current user
    console.log('Testing get current user...');
    const currentUser = await authService.getCurrentUser();
    console.log('✅ Get current user successful:', currentUser);
    
    return { success: true, user: currentUser };
  } catch (error) {
    console.error('❌ Auth flow test failed:', error);
    return { success: false, error };
  }
};

// Test products API
export const testProductsAPI = async () => {
  try {
    // 1. Get all products
    console.log('Testing get all products...');
    const productsResult = await productService.getAllProducts({});
    console.log('✅ Get products successful:', productsResult);
    
    // Lakukan pengujian lainnya jika perlu
    
    return { success: true, products: productsResult };
  } catch (error) {
    console.error('❌ Products API test failed:', error);
    return { success: false, error };
  }
};

// Execute all tests
export const runAllTests = async () => {
  console.log('=== Starting API Integration Tests ===');
  
  // Test connection
  const connectionOk = await testConnection();
  if (!connectionOk) {
    console.error('❌ Integration tests aborted due to connection failure');
    return false;
  }
  
  // Test auth flow
  const authResult = await testAuthFlow();
  
  // Test products API only if auth succeeded
  let productsResult = { success: false };
  if (authResult.success) {
    productsResult = await testProductsAPI();
  }
  
  console.log('=== API Integration Test Results ===');
  console.log(`Auth: ${authResult.success ? '✅ PASS' : '❌ FAIL'}`);
  console.log(`Products: ${productsResult.success ? '✅ PASS' : '❌ FAIL'}`);
  
  return authResult.success && productsResult.success;
};