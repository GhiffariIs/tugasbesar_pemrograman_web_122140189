import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  TextField,
  Grid,
  InputAdornment,
  Typography,
  CircularProgress,
  Alert,
  IconButton,
  Tooltip
} from '@mui/material';
import { 
  Save, 
  Close as CloseIcon,
  Info as InfoIcon 
} from '@mui/icons-material';

const ProductForm = ({ 
  product = null, 
  onSubmit, 
  onCancel, 
  loading = false, 
  error = null,
  buttonText = null 
}) => {
  const [formValues, setFormValues] = useState({
    name: '',
    price: '',
    stock: '',
    minStock: '',
    description: ''
  });

  const [formErrors, setFormErrors] = useState({});
  const [formSubmitted, setFormSubmitted] = useState(false);

  // Initialize form with product data if editing
  useEffect(() => {
    if (product) {
      setFormValues({
        name: product.name || '',
        price: product.price?.toString() || '',
        stock: product.stock?.toString() || '',
        minStock: product.minStock?.toString() || '',
        description: product.description || ''
      });
    } else {
      // Set default values for new product
      setFormValues(prev => ({
        ...prev,
        minStock: '10' // Default min stock value
      }));
    }
  }, [product]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    
    // Handle number inputs
    if (['price', 'stock', 'minStock'].includes(name)) {
      // Allow empty input or non-negative numbers
      if (value === '' || (!isNaN(value) && parseInt(value) >= 0)) {
        setFormValues(prev => ({ ...prev, [name]: value }));
      }
    } else {
      setFormValues(prev => ({ ...prev, [name]: value }));
    }
    
    // Clear validation error when field changes
    if (formErrors[name]) {
      setFormErrors(prev => ({ ...prev, [name]: null }));
    }
  };

  const validateForm = () => {
    const errors = {};
    let isValid = true;

    // Validate required fields
    if (!formValues.name || !formValues.name.trim()) {
      errors.name = 'Product name is required';
      isValid = false;
    }

    if (!formValues.price) {
      errors.price = 'Price is required';
      isValid = false;
    } else {
      const priceValue = parseFloat(formValues.price);
      if (isNaN(priceValue) || priceValue <= 0) {
        errors.price = 'Price must be a number greater than 0';
        isValid = false;
      }
    }

    if (!formValues.stock) {
      errors.stock = 'Stock quantity is required';
      isValid = false;
    } else {
      const stockValue = parseInt(formValues.stock);
      if (isNaN(stockValue) || stockValue < 0) {
        errors.stock = 'Stock must be a non-negative number';
        isValid = false;
      }
    }

    if (!formValues.minStock) {
      errors.minStock = 'Minimum stock is required';
      isValid = false;
    } else {
      const minStockValue = parseInt(formValues.minStock);
      if (isNaN(minStockValue) || minStockValue < 0) {
        errors.minStock = 'Minimum stock must be a non-negative number';
        isValid = false;
      }
    }

    setFormErrors(errors);
    return isValid;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setFormSubmitted(true);

    if (validateForm()) {
      // Ensure all values are properly formatted before submission
      const productData = {
        ...formValues,
        price: parseFloat(formValues.price),
        stock: parseInt(formValues.stock),
        minStock: parseInt(formValues.minStock),
        description: formValues.description || '', // Ensure description is never undefined
      };

      // Log the data to be sent (helpful for debugging)
      console.log('Form data to be submitted:', productData);
      
      onSubmit(productData);
    }
  };

  // Determine what text to show on the submit button
  const getButtonText = () => {
    if (loading) {
      return <CircularProgress size={24} />;
    }
    
    if (buttonText) {
      return buttonText;
    }
    
    return product ? 'Update Product' : 'Add Product';
  };

  return (
    <Box component="form" onSubmit={handleSubmit} noValidate>
      {error && (
        <Alert 
          severity="error" 
          sx={{ mb: 2 }}
          action={
            <IconButton
              aria-label="close"
              color="inherit"
              size="small"
              onClick={() => setFormErrors({})}
            >
              <CloseIcon fontSize="small" />
            </IconButton>
          }
        >
          {error}
        </Alert>
      )}

      {Object.keys(formErrors).length > 0 && formSubmitted && (
        <Alert severity="error" sx={{ mb: 2 }}>
          Please fix the errors below to continue.
        </Alert>
      )}

      <Grid container spacing={2}>
        <Grid item xs={12}>
          <TextField
            fullWidth
            required
            id="name"
            name="name"
            label="Product Name"
            value={formValues.name}
            onChange={handleChange}
            error={!!formErrors.name && formSubmitted}
            helperText={(formSubmitted && formErrors.name) || ''}
            disabled={loading}
            autoFocus
          />
        </Grid>

        {/* Menampilkan info SKU hanya ketika mengedit produk yang sudah ada */}
        {product && product.id && (
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              id="sku"
              name="sku"
              label="SKU"
              value={`PRD-${product.id}`}
              disabled
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <Tooltip title="This SKU is automatically generated from the product ID">
                      <InfoIcon fontSize="small" color="action" />
                    </Tooltip>
                  </InputAdornment>
                ),
              }}
            />
          </Grid>
        )}

        <Grid item xs={12} sm={product && product.id ? 6 : 12}>
          <TextField
            fullWidth
            required
            id="price"
            name="price"
            label="Price"
            value={formValues.price}
            onChange={handleChange}
            error={!!formErrors.price && formSubmitted}
            helperText={(formSubmitted && formErrors.price) || ''}
            disabled={loading}
            InputProps={{
              startAdornment: <InputAdornment position="start">Rp</InputAdornment>,
            }}
          />
        </Grid>

        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            required
            id="stock"
            name="stock"
            label="Stock Quantity"
            value={formValues.stock}
            onChange={handleChange}
            error={!!formErrors.stock && formSubmitted}
            helperText={(formSubmitted && formErrors.stock) || ''}
            disabled={loading}
          />
        </Grid>

        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            required
            id="minStock"
            name="minStock"
            label="Minimum Stock"
            value={formValues.minStock}
            onChange={handleChange}
            error={!!formErrors.minStock && formSubmitted}
            helperText={(formSubmitted && formErrors.minStock) || "Alert will show when stock falls below this level"}
            disabled={loading}
          />
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            id="description"
            name="description"
            label="Description"
            multiline
            rows={3}
            value={formValues.description}
            onChange={handleChange}
            disabled={loading}
          />
        </Grid>
      </Grid>

      <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 3, gap: 1 }}>
        <Button 
          type="button" 
          onClick={onCancel} 
          disabled={loading}
          startIcon={<CloseIcon />}
        >
          Cancel
        </Button>
        <Button 
          type="submit" 
          variant="contained" 
          color="primary"
          disabled={loading}
          startIcon={loading ? null : <Save />}
        >
          {getButtonText()}
        </Button>
      </Box>
    </Box>
  );
};

export default ProductForm;
