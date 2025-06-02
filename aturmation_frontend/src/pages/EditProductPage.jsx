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
  Grid,
  Chip,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
} from '@mui/material';
import { 
  Save as SaveIcon,
  Cancel as CancelIcon,
  Restore as RestoreIcon,
  Warning as WarningIcon,
  Check as CheckIcon
} from '@mui/icons-material';
import { useNavigate, useParams } from 'react-router-dom';
import { productService } from '../services/services';
import ProductForm from '../components/products/ProductForm';

const EditProductPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);
  const [originalProduct, setOriginalProduct] = useState(null); // Store original data for comparison
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [resetDialogOpen, setResetDialogOpen] = useState(false);
  
  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const data = await productService.getProductById(id);
        setProduct(data);
        setOriginalProduct(data); // Save original data for reset functionality
      } catch (err) {
        console.error('Error fetching product:', err);
        setError('Failed to load product details. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [id]);

  const handleSubmit = async (productData) => {
    setSaving(true);
    setError(null);
    
    try {
      await productService.updateProduct(id, productData);
      setSuccess(true);
      
      // Update the local product data with the new values
      setProduct(productData);
      
      // Navigate back to products after successful update
      setTimeout(() => {
        navigate('/products');
      }, 2000);
    } catch (err) {
      console.error('Error updating product:', err);
      setError(err.response?.data?.message || 'Failed to update product. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    navigate('/products');
  };

  const handleResetData = () => {
    setResetDialogOpen(true);
  };

  const confirmReset = () => {
    setProduct({...originalProduct}); // Reset to original data
    setResetDialogOpen(false);
  };

  const getStockStatusChip = (product) => {
    const minStock = product.minStock || 10;
    
    if (product.stock === 0) {
      return <Chip
        color="error" 
        icon={<WarningIcon />} 
        label="Out of stock" 
      />;
    } else if (product.stock <= minStock) {
      return <Chip 
        color="warning" 
        icon={<WarningIcon />} 
        label="Low stock" 
      />;
    } else {
      return <Chip 
        color="success" 
        icon={<CheckIcon />} 
        label="In stock" 
      />;
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (!product && !loading) {
    return (
      <Box>
        <Alert severity="error">
          Product not found or you don't have permission to edit it.
        </Alert>
        <Button 
          variant="contained"
          onClick={() => navigate('/products')}
          sx={{ mt: 2 }}
        >
          Back to Products
        </Button>
      </Box>
    );
  }

  return (
    <Box>
      <Breadcrumbs sx={{ mb: 2 }}>
        <Link color="inherit" href="/" onClick={(e) => {
          e.preventDefault();
          navigate('/');
        }}>
          Dashboard
        </Link>
        <Link color="inherit" href="/products" onClick={(e) => {
          e.preventDefault();
          navigate('/products');
        }}>
          Products
        </Link>
        <Link color="inherit" onClick={(e) => {
          e.preventDefault();
          navigate(`/products/${id}`);
        }}>
          {originalProduct?.name}
        </Link>
        <Typography color="text.primary">Edit</Typography>
      </Breadcrumbs>

      <Box
        display="flex"
        justifyContent="space-between"
        alignItems="center"
        mb={3}
      >
        <Typography variant="h4" component="h1">
          Edit Product
        </Typography>
        <Button
          variant="outlined"
          startIcon={<RestoreIcon />}
          onClick={handleResetData}
          disabled={saving}
        >
          Reset to Original
        </Button>
      </Box>

      {/* Product current information summary */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Current Product Information
        </Typography>
        <Grid container spacing={2} sx={{ mb: 2 }}>
          <Grid item xs={12} sm={6}>
            <Typography variant="body2" color="text.secondary">
              Product Name
            </Typography>
            <Typography variant="body1" fontWeight="medium">
              {originalProduct?.name}
            </Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Typography variant="body2" color="text.secondary">
              SKU
            </Typography>
            <Typography variant="body1">
              {originalProduct?.id ? `PRD-${originalProduct.id}` : 'N/A'}
            </Typography>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Typography variant="body2" color="text.secondary">
              Price
            </Typography>
            <Typography variant="body1" fontWeight="medium">
              Rp {originalProduct?.price?.toLocaleString()}
            </Typography>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Typography variant="body2" color="text.secondary">
              Current Stock
            </Typography>
            <Box display="flex" alignItems="center">
              <Typography variant="body1" sx={{ mr: 1 }}>
                {originalProduct?.stock} units
              </Typography>
              {getStockStatusChip(originalProduct)}
            </Box>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Typography variant="body2" color="text.secondary">
              Minimum Stock Level
            </Typography>
            <Typography variant="body1">
              {originalProduct?.minStock || 10} units
            </Typography>
          </Grid>
        </Grid>
        <Divider sx={{ my: 2 }} />
        <Typography variant="body2" color="text.secondary" gutterBottom>
          Description
        </Typography>
        <Typography variant="body1">
          {originalProduct?.description || "No description provided."}
        </Typography>
      </Paper>

      {/* Product edit form */}
      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Update Information
        </Typography>
        <Divider sx={{ mb: 3 }} />
        
        <ProductForm 
          product={product} 
          onSubmit={handleSubmit} 
          onCancel={handleCancel} 
          loading={saving}
          error={error}
          buttonText="Update Product"
        />
      </Paper>

      {/* Success notification */}
      <Snackbar
        open={success}
        autoHideDuration={2000}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert severity="success" variant="filled">
          Product updated successfully
        </Alert>
      </Snackbar>

      {/* Reset confirmation dialog */}
      <Dialog
        open={resetDialogOpen}
        onClose={() => setResetDialogOpen(false)}
        aria-labelledby="reset-dialog-title"
      >
        <DialogTitle id="reset-dialog-title">
          Reset Form?
        </DialogTitle>
        <DialogContent>
          <DialogContentText>
            This will reset all form fields to their original values. Any changes you've made will be lost.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setResetDialogOpen(false)}>Cancel</Button>
          <Button onClick={confirmReset} variant="contained" color="primary">
            Reset Form
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default EditProductPage;