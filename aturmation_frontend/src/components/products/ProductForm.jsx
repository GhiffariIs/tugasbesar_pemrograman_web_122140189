import React, { useState, useEffect } from 'react';
import {
  Grid,
  TextField,
  Box,
  Button,
  InputAdornment,
  CircularProgress,
  Alert,
  Typography,
  useTheme,
  useMediaQuery,
  Paper,
  FormHelperText,
} from '@mui/material';
import { generateProductCode } from '../../utils/formatters';

const ProductForm = ({ product, onSave, loading, isEdit = false, onCancel }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  
  const [formData, setFormData] = useState({
    name: '',
    sku: '',
    price: '',
    stock: '',
    minStock: '10', // Default min stock value
    description: ''
  });
  
  const [errors, setErrors] = useState({});
  const [formChanged, setFormChanged] = useState(false);
  
  useEffect(() => {
    if (product && isEdit) {
      setFormData({
        name: product.name || '',
        sku: product.sku || '',
        price: product.price || '',
        stock: product.stock || '',
        minStock: product.minStock || '10',
        description: product.description || ''
      });
    } else if (!isEdit) {
      // Generate SKU for new products
      setFormData(prev => ({
        ...prev,
        sku: generateProductCode()
      }));
    }
  }, [product, isEdit]);
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    
    // Handle number inputs
    if (['price', 'stock', 'minStock'].includes(name)) {
      // Allow only positive numbers or empty string
      const numValue = value === '' ? '' : Math.max(0, Number(value));
      setFormData(prev => ({
        ...prev,
        [name]: numValue
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: value
      }));
    }
    
    // Clear validation error when field changes
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
    
    setFormChanged(true);
  };
  
  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.name.trim()) {
      newErrors.name = 'Product name is required';
    }
    
    if (!formData.sku.trim()) {
      newErrors.sku = 'SKU is required';
    }
    
    if (!formData.price) {
      newErrors.price = 'Price is required';
    } else if (formData.price <= 0) {
      newErrors.price = 'Price must be greater than 0';
    }
    
    if (formData.stock === '') {
      newErrors.stock = 'Stock quantity is required';
    }
    
    if (formData.minStock === '') {
      newErrors.minStock = 'Minimum stock is required';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (validateForm()) {
      const productData = {
        ...formData,
        price: Number(formData.price),
        stock: Number(formData.stock),
        minStock: Number(formData.minStock),
      };
      
      onSave(productData);
    }
  };
  
  const generateNewSku = () => {
    setFormData(prev => ({
      ...prev,
      sku: generateProductCode()
    }));
    setFormChanged(true);
  };
  
  return (
    <Paper elevation={0} sx={{ p: isMobile ? 2 : 3 }}>
      <Box component="form" onSubmit={handleSubmit} noValidate>
        <Typography variant="h6" mb={2}>
          {isEdit ? 'Edit Product' : 'Add New Product'}
        </Typography>
        
        {Object.keys(errors).length > 0 && (
          <Alert severity="error" sx={{ mb: 2 }}>
            Please correct the errors below to continue
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
              value={formData.name}
              onChange={handleChange}
              error={Boolean(errors.name)}
              helperText={errors.name}
              disabled={loading}
              autoFocus={!isEdit}
            />
          </Grid>
          
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              required
              id="sku"
              name="sku"
              label="SKU / Product Code"
              value={formData.sku}
              onChange={handleChange}
              error={Boolean(errors.sku)}
              helperText={errors.sku}
              disabled={loading || isEdit}
              InputProps={{
                endAdornment: !isEdit && (
                  <InputAdornment position="end">
                    <Button
                      onClick={generateNewSku}
                      size="small"
                      disabled={loading}
                    >
                      Generate
                    </Button>
                  </InputAdornment>
                ),
              }}
            />
          </Grid>
          
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              required
              id="price"
              name="price"
              label="Price"
              value={formData.price}
              onChange={handleChange}
              error={Boolean(errors.price)}
              helperText={errors.price}
              disabled={loading}
              type="number"
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
              label="Stock"
              value={formData.stock}
              onChange={handleChange}
              error={Boolean(errors.stock)}
              helperText={errors.stock}
              disabled={loading}
              type="number"
            />
          </Grid>
          
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              required
              id="minStock"
              name="minStock"
              label="Minimum Stock"
              value={formData.minStock}
              onChange={handleChange}
              error={Boolean(errors.minStock)}
              helperText={errors.minStock || "Notification will appear when stock falls below this value"}
              disabled={loading}
              type="number"
            />
          </Grid>
          
          <Grid item xs={12}>
            <TextField
              fullWidth
              id="description"
              name="description"
              label="Description"
              value={formData.description}
              onChange={handleChange}
              disabled={loading}
              multiline
              rows={3}
            />
          </Grid>
          
          <Grid item xs={12} sx={{ mt: 2, display: 'flex', justifyContent: isMobile ? 'center' : 'flex-end', flexDirection: isMobile ? 'column' : 'row', gap: 2 }}>
            <Button 
              variant="outlined" 
              onClick={onCancel} 
              disabled={loading}
              fullWidth={isMobile}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="contained"
              color="primary"
              disabled={loading || (!formChanged && isEdit)}
              fullWidth={isMobile}
            >
              {loading ? (
                <CircularProgress size={24} />
              ) : isEdit ? (
                'Save Changes'
              ) : (
                'Add Product'
              )}
            </Button>
          </Grid>
        </Grid>
      </Box>
    </Paper>
  );
};

export default ProductForm;
