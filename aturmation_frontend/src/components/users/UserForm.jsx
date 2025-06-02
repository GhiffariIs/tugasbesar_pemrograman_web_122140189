import React, { useState } from 'react';
import {
  Box, TextField, Button, Grid, Typography, FormControl,
  InputLabel, Select, MenuItem, FormHelperText
} from '@mui/material';

const UserForm = ({ initialData = {}, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    name: initialData.name || '',
    username: initialData.username || '',
    email: initialData.email || '',
    role: initialData.role || 'staff',
    password: '',
    confirmPassword: ''
  });
  
  const [errors, setErrors] = useState({});
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    
    // Clear error when field is edited
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };
  
  const validate = () => {
    const newErrors = {};
    
    if (!formData.name.trim()) newErrors.name = 'Name is required';
    if (!formData.username.trim()) newErrors.username = 'Username is required';
    
    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/^\S+@\S+\.\S+$/.test(formData.email)) {
      newErrors.email = 'Invalid email format';
    }
    
    // Only validate password for new user
    if (!initialData.id) {
      if (!formData.password) newErrors.password = 'Password is required';
      else if (formData.password.length < 6) {
        newErrors.password = 'Password must be at least 6 characters';
      }
      
      if (formData.password !== formData.confirmPassword) {
        newErrors.confirmPassword = 'Passwords do not match';
      }
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (validate()) {
      // Omit confirmPassword and exclude password if empty
      const { confirmPassword, ...userData } = formData;
      
      if (!userData.password && initialData.id) {
        delete userData.password;
      }
      
      onSubmit(userData);
    }
  };
  
  return (
    <Box component="form" onSubmit={handleSubmit} noValidate>
      <Typography variant="h6" mb={2}>
        {initialData.id ? 'Edit User' : 'Add New User'}
      </Typography>
      
      <Grid container spacing={2}>
        <Grid xs={12}>
          <TextField
            fullWidth
            label="Name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            error={!!errors.name}
            helperText={errors.name}
            margin="normal"
            required
          />
        </Grid>
        
        <Grid xs={12} sm={6}>
          <TextField
            fullWidth
            label="Username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            error={!!errors.username}
            helperText={errors.username}
            margin="normal"
            required
            disabled={!!initialData.id} // Cannot change username for existing user
          />
        </Grid>
        
        <Grid xs={12} sm={6}>
          <TextField
            fullWidth
            label="Email"
            name="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
            error={!!errors.email}
            helperText={errors.email}
            margin="normal"
            required
          />
        </Grid>
        
        <Grid xs={12} sm={6}>
          <FormControl fullWidth margin="normal">
            <InputLabel id="role-label">Role</InputLabel>
            <Select
              labelId="role-label"
              name="role"
              value={formData.role}
              onChange={handleChange}
              label="Role"
            >
              <MenuItem value="admin">Admin</MenuItem>
              <MenuItem value="staff">Staff</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        
        <Grid xs={12} sm={6}>
          <TextField
            fullWidth
            label={initialData.id ? "New Password (leave empty to keep current)" : "Password"}
            name="password"
            type="password"
            value={formData.password}
            onChange={handleChange}
            error={!!errors.password}
            helperText={errors.password}
            margin="normal"
            required={!initialData.id}
          />
        </Grid>
        
        {(!initialData.id || formData.password) && (
          <Grid xs={12}>
            <TextField
              fullWidth
              label="Confirm Password"
              name="confirmPassword"
              type="password"
              value={formData.confirmPassword}
              onChange={handleChange}
              error={!!errors.confirmPassword}
              helperText={errors.confirmPassword}
              margin="normal"
              required={!initialData.id || !!formData.password}
            />
          </Grid>
        )}
        
        <Grid xs={12} mt={2} display="flex" justifyContent="flex-end">
          <Button 
            variant="outlined" 
            onClick={onCancel} 
            sx={{ mr: 1 }}
          >
            Cancel
          </Button>
          <Button 
            type="submit" 
            variant="contained" 
            color="primary"
          >
            {initialData.id ? 'Update' : 'Save'}
          </Button>
        </Grid>
      </Grid>
    </Box>
  );
};

export default UserForm;