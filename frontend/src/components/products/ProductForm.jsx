import { useState, useEffect } from 'react';
import {
  Grid,
  TextField,
  Box,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormHelperText,
  InputAdornment,
  CircularProgress,
  Alert
} from '@mui/material';
import { generateProductCode } from '../../utils/formatters';

const ProductForm = ({ product, categories, onSave, loading, isEdit = false }) => {
  const [formData, setFormData] = useState({
    name: '',
    sku: '',
    price: '',
    stock: '',
    minStock: '',
    categoryId: '',
    description: ''
  });
  
  const [errors, setErrors] = useState({});
  
  useEffect(() => {
    if (product && isEdit) {
      setFormData({
        name: product.name || '',
        sku: product.sku || '',
        price: product.price || '',
        stock: product.stock || '',
        minStock: product.minStock || '',
        categoryId: product.category?.id || '',
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
  };
  
  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.name.trim()) {
      newErrors.name = 'Nama produk tidak boleh kosong';
    }
    
    if (!formData.sku.trim()) {
      newErrors.sku = 'SKU tidak boleh kosong';
    }
    
    if (!formData.price) {
      newErrors.price = 'Harga tidak boleh kosong';
    } else if (formData.price <= 0) {
      newErrors.price = 'Harga harus lebih dari 0';
    }
    
    if (formData.stock === '') {
      newErrors.stock = 'Stok tidak boleh kosong';
    }
    
    if (formData.minStock === '') {
      newErrors.minStock = 'Stok minimal tidak boleh kosong';
    }
    
    if (!formData.categoryId) {
      newErrors.categoryId = 'Kategori harus dipilih';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (validateForm()) {
      // Transform category ID to match API expectations
      const selectedCategory = categories.find(c => c.id === parseInt(formData.categoryId));
      
      const productData = {
        ...formData,
        price: Number(formData.price),
        stock: Number(formData.stock),
        minStock: Number(formData.minStock),
        category: selectedCategory
      };
      
      onSave(productData);
    }
  };
  
  const generateNewSku = () => {
    setFormData(prev => ({
      ...prev,
      sku: generateProductCode()
    }));
  };
  
  return (
    <Box component="form" onSubmit={handleSubmit} noValidate>
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <TextField
            fullWidth
            required
            id="name"
            name="name"
            label="Nama Produk"
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
            label="SKU / Kode Produk"
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
              )
            }}
          />
        </Grid>
        
        <Grid item xs={12} sm={6}>
          <FormControl fullWidth required error={Boolean(errors.categoryId)}>
            <InputLabel id="category-label">Kategori</InputLabel>
            <Select
              labelId="category-label"
              id="categoryId"
              name="categoryId"
              value={formData.categoryId}
              label="Kategori"
              onChange={handleChange}
              disabled={loading}
            >
              {categories.map((category) => (
                <MenuItem key={category.id} value={category.id}>
                  {category.name}
                </MenuItem>
              ))}
            </Select>
            {errors.categoryId && (
              <FormHelperText>{errors.categoryId}</FormHelperText>
            )}
          </FormControl>
        </Grid>
        
        <Grid item xs={12} sm={4}>
          <TextField
            fullWidth
            required
            id="price"
            name="price"
            label="Harga"
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
        
        <Grid item xs={12} sm={4}>
          <TextField
            fullWidth
            required
            id="stock"
            name="stock"
            label="Stok"
            value={formData.stock}
            onChange={handleChange}
            error={Boolean(errors.stock)}
            helperText={errors.stock}
            disabled={loading}
            type="number"
          />
        </Grid>
        
        <Grid item xs={12} sm={4}>
          <TextField
            fullWidth
            required
            id="minStock"
            name="minStock"
            label="Stok Minimal"
            value={formData.minStock}
            onChange={handleChange}
            error={Boolean(errors.minStock)}
            helperText={errors.minStock || "Notifikasi akan muncul jika stok di bawah nilai ini"}
            disabled={loading}
            type="number"
          />
        </Grid>
        
        <Grid item xs={12}>
          <TextField
            fullWidth
            id="description"
            name="description"
            label="Deskripsi"
            value={formData.description}
            onChange={handleChange}
            disabled={loading}
            multiline
            rows={3}
          />
        </Grid>
        
        <Grid item xs={12}>
          <Button
            type="submit"
            variant="contained"
            fullWidth
            size="large"
            disabled={loading}
            sx={{ mt: 1 }}
          >
            {loading ? (
              <CircularProgress size={24} />
            ) : isEdit ? (
              'Simpan Perubahan'
            ) : (
              'Tambah Produk'
            )}
          </Button>
        </Grid>
      </Grid>
    </Box>
  );
};

export default ProductForm;
