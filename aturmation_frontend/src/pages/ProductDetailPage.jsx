import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Divider,
  Button,
  Chip,
  CircularProgress,
  Alert,
  Card,
  CardContent,
  IconButton,
  Dialog,
} from '@mui/material';
import { ArrowBack, Edit as EditIcon } from '@mui/icons-material';
import { useParams, useNavigate } from 'react-router-dom';
import { productService } from '../services/services';
import ProductForm from '../components/products/ProductForm';

const ProductDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [openEditDialog, setOpenEditDialog] = useState(false);

  useEffect(() => {
    const fetchProduct = async () => {
      setLoading(true);
      try {
        const data = await productService.getProductById(id);
        setProduct(data);
      } catch (err) {
        console.error('Error fetching product details:', err);
        setError('Failed to load product details');
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [id]);

  const handleUpdateProduct = async (updatedData) => {
    setLoading(true);
    try {
      const updated = await productService.updateProduct(id, updatedData);
      setProduct(updated);
      setOpenEditDialog(false);
    } catch (err) {
      console.error('Error updating product:', err);
      setError('Failed to update product');
    } finally {
      setLoading(false);
    }
  };

  const handleGoBack = () => {
    navigate('/products');
  };

  if (loading && !product) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box p={3}>
        <Alert severity="error">{error}</Alert>
        <Button 
          startIcon={<ArrowBack />} 
          onClick={handleGoBack} 
          sx={{ mt: 2 }}
        >
          Back to Products
        </Button>
      </Box>
    );
  }

  return (
    <Box>
      <Box display="flex" alignItems="center" mb={3}>
        <IconButton onClick={handleGoBack} sx={{ mr: 1 }}>
          <ArrowBack />
        </IconButton>
        <Typography variant="h4" component="h1">
          Product Details
        </Typography>
        <Box flexGrow={1} />
        <Button
          startIcon={<EditIcon />}
          variant="contained"
          onClick={() => setOpenEditDialog(true)}
        >
          Edit Product
        </Button>
      </Box>

      {product && (
        <Paper elevation={2} sx={{ p: 3, mb: 4 }}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Typography variant="h5" gutterBottom>
                {product.name}
              </Typography>
              <Typography variant="subtitle1" color="textSecondary">
                SKU: {product.sku}
              </Typography>
              <Chip 
                label={product.stock > 0 ? 'In Stock' : 'Out of Stock'} 
                color={product.stock > 0 ? 'success' : 'error'} 
                size="small"
                sx={{ mt: 1 }}
              />
            </Grid>

            <Grid item xs={12}>
              <Divider />
            </Grid>

            <Grid item xs={12} md={6}>
              <Typography variant="subtitle2" color="textSecondary">
                Price
              </Typography>
              <Typography variant="h6">
                Rp {product.price?.toLocaleString()}
              </Typography>
            </Grid>

            <Grid item xs={12} md={6}>
              <Typography variant="subtitle2" color="textSecondary">
                Stock
              </Typography>
              <Typography variant="h6">
                {product.stock} units
              </Typography>
            </Grid>

            <Grid item xs={12}>
              <Divider />
            </Grid>

            <Grid item xs={12}>
              <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                Description
              </Typography>
              <Typography variant="body1" paragraph>
                {product.description || 'No description available'}
              </Typography>
            </Grid>
          </Grid>
        </Paper>
      )}

      <Dialog 
        open={openEditDialog} 
        onClose={() => setOpenEditDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <Box p={3}>
          <ProductForm
            initialData={product}
            onSubmit={handleUpdateProduct}
            onCancel={() => setOpenEditDialog(false)}
          />
        </Box>
      </Dialog>
    </Box>
  );
};

export default ProductDetailPage;