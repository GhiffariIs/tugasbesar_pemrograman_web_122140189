import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Breadcrumbs,
  Link,
  CircularProgress,
  Snackbar,
  Alert,
  Divider,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { productService } from '../services/services';
import ProductForm from '../components/products/ProductForm';

const AddProductPage = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    // Cek struktur produk yang diharapkan backend
    const checkProductStructure = async () => {
      try {
        // Mengambil salah satu produk untuk melihat strukturnya
        const response = await productService.getAllProducts({ limit: 1 });
        if (response && response.data && response.data.length > 0) {
          console.log('Product structure from backend:', response.data[0]);
        }
      } catch (err) {
        console.error('Failed to get product structure:', err);
      }
    };
    
    checkProductStructure();
  }, []);

  const handleSubmit = async (productData) => {
    setLoading(true);
    setError(null);

    try {
      // Log data for debugging
      console.log('Raw product data before submit:', productData);
      
      // Ensure data format matches what backend expects
      const formattedData = {
        name: productData.name,
        sku: `TEMP-${Date.now()}`, // Provide temporary SKU
        price: Number(productData.price),
        stock: Number(productData.stock),
        minStock: Number(productData.minStock),
        description: productData.description || '',
      };
      
      console.log('Formatted data to send:', formattedData);
      
      await productService.createProduct(formattedData);
      
      setSuccess(true);
      
      // Navigate back to products after successful creation
      setTimeout(() => {
        navigate('/products');
      }, 2000);
    } catch (err) {
      // Detailed error logging
      console.error('Error adding product:', err);
      
      if (err.response) {
        console.error('Server responded with error:', {
          status: err.response.status,
          statusText: err.response.statusText,
          data: err.response.data,
          requestData: err.config?.data ? JSON.parse(err.config.data) : 'No data'
        });
        
        setError(
          err.response.data?.message || 
          err.response.data?.error || 
          `Server error (${err.response.status}): Please check the console for details`
        );
      } else if (err.request) {
        setError('No response received from server. Please check your network connection.');
      } else {
        setError(`Error: ${err.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    navigate('/products');
  };

  return (
    <Box>
      <Breadcrumbs sx={{ mb: 2 }}>
        <Link
          color="inherit"
          href="/"
          onClick={(e) => {
            e.preventDefault();
            navigate('/');
          }}
        >
          Dashboard
        </Link>
        <Link
          color="inherit"
          href="/products"
          onClick={(e) => {
            e.preventDefault();
            navigate('/products');
          }}
        >
          Products
        </Link>
        <Typography color="text.primary">Add Product</Typography>
      </Breadcrumbs>

      <Typography variant="h4" component="h1" sx={{ mb: 3 }}>
        Add New Product
      </Typography>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Product Information
        </Typography>
        <Divider sx={{ mb: 3 }} />

        <ProductForm
          onSubmit={handleSubmit}
          onCancel={handleCancel}
          loading={loading}
          error={error}
          buttonText="Add Product"
        />
      </Paper>

      <Snackbar
        open={success}
        autoHideDuration={2000}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert severity="success" variant="filled">
          Product added successfully
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default AddProductPage;