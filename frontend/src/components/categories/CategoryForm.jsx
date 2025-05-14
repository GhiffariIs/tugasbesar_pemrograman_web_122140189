import { useState, useEffect } from 'react';
import {
  Grid,
  TextField,
  Box,
  Button,
  CircularProgress
} from '@mui/material';

const CategoryForm = ({ category, onSave, loading, isEdit = false }) => {
  const [formData, setFormData] = useState({
    name: '',
    description: ''
  });
  
  const [errors, setErrors] = useState({});
  
  useEffect(() => {
    if (category && isEdit) {
      setFormData({
        name: category.name || '',
        description: category.description || ''
      });
    }
  }, [category, isEdit]);
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
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
      newErrors.name = 'Nama kategori tidak boleh kosong';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (validateForm()) {
      onSave(formData);
    }
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
            label="Nama Kategori"
            value={formData.name}
            onChange={handleChange}
            error={Boolean(errors.name)}
            helperText={errors.name}
            disabled={loading}
            autoFocus
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
              'Tambah Kategori'
            )}
          </Button>
        </Grid>
      </Grid>
    </Box>
  );
};

export default CategoryForm;
