import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Grid, 
  Chip,
  Button,
  Divider,
  CircularProgress,
  Breadcrumbs,
  Link,
  Alert,
  IconButton
} from '@mui/material';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  ArrowBack as ArrowBackIcon,
  Check as CheckIcon,
  Warning as WarningIcon
} from '@mui/icons-material';
import { useNavigate, useParams } from 'react-router-dom';
import { productService } from '../services/services';

const ProductDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const data = await productService.getProductById(id);
        setProduct(data);
      } catch (err) {
        console.error('Error fetching product:', err);
        setError('Failed to load product details');
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [id]);

  const handleEdit = () => {
    navigate(`/products/${id}/edit`);
  };

  const handleBack = () => {
    navigate('/products');
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

  if (error) {
    return (
      <Box>
        <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>
        <Button 
          startIcon={<ArrowBackIcon />}
          onClick={handleBack}
        >
          Back to Products
        </Button>
      </Box>
    );
  }

  if (!product) {
    return (
      <Box>
        <Alert severity="warning" sx={{ mb: 2 }}>Product not found</Alert>
        <Button 
          startIcon={<ArrowBackIcon />}
          onClick={handleBack}
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
        <Typography color="text.primary">{product.name}</Typography>
      </Breadcrumbs>

      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box display="flex" alignItems="center">
          <IconButton onClick={handleBack} sx={{ mr: 1 }}>
            <ArrowBackIcon />
          </IconButton>
          <Typography variant="h4" component="h1">
            Product Details
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<EditIcon />}
          onClick={handleEdit}
        >
          Edit
        </Button>
      </Box>

      <Paper sx={{ p: 3 }}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Typography variant="h5" gutterBottom>
              {product.name}
            </Typography>
            <Box display="flex" alignItems="center" mb={2}>
              <Typography variant="body2" color="text.secondary" sx={{ mr: 2 }}>
                SKU: {product.id ? `PRD-${product.id}` : 'N/A'}
              </Typography>
              {getStockStatusChip(product)}
            </Box>
            <Divider sx={{ my: 2 }} />
          </Grid>

          <Grid item xs={12} md={6}>
            <Typography variant="subtitle1" gutterBottom fontWeight="bold">
              Price
            </Typography>
            <Typography variant="h4" color="primary" gutterBottom>
              Rp {(product.price || 0).toLocaleString()}
            </Typography>
          </Grid>

          <Grid item xs={12} md={6}>
            <Typography variant="subtitle1" gutterBottom fontWeight="bold">
              Stock Information
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <Typography variant="body2" color="text.secondary">
                  Current Stock
                </Typography>
                <Typography variant="h6">
                  {product.stock} units
                </Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography variant="body2" color="text.secondary">
                  Minimum Stock
                </Typography>
                <Typography variant="h6">
                  {product.minStock || 10} units
                </Typography>
              </Grid>
            </Grid>
          </Grid>

          <Grid item xs={12}>
            <Divider sx={{ my: 2 }} />
            <Typography variant="subtitle1" gutterBottom fontWeight="bold">
              Description
            </Typography>
            <Typography variant="body1" paragraph>
              {product.description || 'No description provided.'}
            </Typography>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
};

export default ProductDetailPage;