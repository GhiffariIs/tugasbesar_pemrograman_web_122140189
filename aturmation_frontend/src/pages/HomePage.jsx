import React, { useState, useEffect } from 'react';
import {
  Box, 
  Typography, 
  Grid, 
  Card, 
  CardContent,
  Divider,
  CircularProgress,
  Paper,
  Button,
  List,
  ListItem,
  ListItemText,
  Chip,
  Avatar,
  Alert,
  useTheme
} from '@mui/material';
import {
  Inventory as InventoryIcon,
  Warning as WarningIcon,
  Add as AddIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { productService } from '../services/services';

const HomePage = () => {
  const theme = useTheme();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [productStats, setProductStats] = useState({
    totalProducts: 0,
    lowStockProducts: [],
    recentProducts: [],
    highestPricedProducts: []
  });

  useEffect(() => {
    const fetchProductData = async () => {
      setLoading(true);
      try {
        // Fetch products data
        const productsResponse = await productService.getAllProducts({});
        
        // Extract products array from response based on structure
        let products = [];
        if (Array.isArray(productsResponse)) {
          products = productsResponse;
        } else if (productsResponse?.products && Array.isArray(productsResponse.products)) {
          products = productsResponse.products;
        } else if (productsResponse?.data && Array.isArray(productsResponse.data)) {
          products = productsResponse.data;
        }
        
        // Calculate statistics
        const totalProducts = products.length;
        
        // Get low stock products (stock <= minStock or <= 10 if minStock not defined)
        const lowStockProducts = products
          .filter(p => p.stock <= (p.minStock || 10))
          .sort((a, b) => a.stock - b.stock)
          .slice(0, 5);
        
        // Get 5 most recent products
        const recentProducts = [...products]
          .sort((a, b) => {
            if (a.createdAt && b.createdAt) {
              return new Date(b.createdAt) - new Date(a.createdAt);
            }
            return b.id - a.id; // Fallback to ID if createdAt is not available
          })
          .slice(0, 5);
        
        // Get 5 highest priced products
        const highestPricedProducts = [...products]
          .sort((a, b) => (b.price || 0) - (a.price || 0))
          .slice(0, 5);
        
        setProductStats({
          totalProducts,
          lowStockProducts,
          recentProducts,
          highestPricedProducts
        });
      } catch (err) {
        console.error('Error fetching product data:', err);
        setError('Failed to load product data');
      } finally {
        setLoading(false);
      }
    };
    
    fetchProductData();
  }, []);

  if (loading) {
    return (
      <Box sx={{ width: '100%', mt: 4, display: 'flex', justifyContent: 'center' }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Box mb={4}>
        <Typography variant="h4" gutterBottom>
          Inventory Dashboard
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Product overview and inventory status
        </Typography>
      </Box>
      
      {/* Inventory Summary */}
      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} md={4}>
          <Card variant="outlined" sx={{ height: '100%' }}>
            <CardContent>
              <Box display="flex" alignItems="center" mb={1}>
                <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
                  <InventoryIcon />
                </Avatar>
                <Typography variant="h6">
                  Total Products
                </Typography>
              </Box>
              <Typography variant="h3" gutterBottom fontWeight="bold">
                {productStats.totalProducts}
              </Typography>
              <Button 
                variant="text" 
                onClick={() => navigate('/products')}
                sx={{ mt: 1 }}
              >
                View all products
              </Button>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={8}>
          <Card variant="outlined" sx={{ height: '100%' }}>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <Avatar sx={{ bgcolor: 'warning.main', mr: 2 }}>
                  <WarningIcon />
                </Avatar>
                <Typography variant="h6">
                  Low Stock Alert
                </Typography>
              </Box>
              
              {productStats.lowStockProducts.length > 0 ? (
                <List dense disablePadding>
                  {productStats.lowStockProducts.map((product) => (
                    <ListItem
                      key={product.id}
                      button
                      onClick={() => navigate(`/products/${product.id}`)}
                      sx={{ 
                        borderRadius: 1,
                        mb: 1,
                        bgcolor: product.stock === 0 ? 'error.lighter' : 'warning.lighter',
                        ':hover': { bgcolor: product.stock === 0 ? 'error.light' : 'warning.light' }
                      }}
                    >
                      <ListItemText
                        primary={
                          <Box display="flex" justifyContent="space-between" alignItems="center">
                            <Typography variant="body1" fontWeight="medium">
                              {product.name}
                            </Typography>
                            <Chip 
                              size="small"
                              label={product.stock === 0 ? 'Out of stock' : 'Low stock'} 
                              color={product.stock === 0 ? 'error' : 'warning'}
                            />
                          </Box>
                        }
                        secondary={`Stock: ${product.stock} | SKU: ${product.sku}`}
                      />
                    </ListItem>
                  ))}
                </List>
              ) : (
                <Typography>All products are well-stocked.</Typography>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Recent Products */}
      <Paper variant="outlined" sx={{ mb: 4 }}>
        <Box p={2} display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="h6">Recent Products</Typography>
          <Button 
            variant="contained" 
            size="small" 
            startIcon={<AddIcon />}
            onClick={() => navigate('/products')}
          >
            Add Product
          </Button>
        </Box>
        <Divider />
        
        {productStats.recentProducts.length > 0 ? (
          <List disablePadding>
            {productStats.recentProducts.map((product, index) => (
              <React.Fragment key={product.id}>
                <ListItem 
                  button 
                  onClick={() => navigate(`/products/${product.id}`)}
                  sx={{ px: 2, py: 1.5 }}
                >
                  <ListItemText
                    primary={product.name}
                    secondary={
                      <Box component="span" display="flex" justifyContent="space-between" alignItems="center">
                        <span>SKU: {product.sku}</span>
                        <span>
                          <Chip 
                            size="small" 
                            label={`${product.stock} in stock`} 
                            color={product.stock <= (product.minStock || 10) ? 'warning' : 'success'}
                            variant="outlined"
                          />
                        </span>
                      </Box>
                    }
                  />
                  <Typography variant="body1" color="primary" sx={{ fontWeight: 'bold', ml: 2 }}>
                    Rp {product.price?.toLocaleString()}
                  </Typography>
                </ListItem>
                {index < productStats.recentProducts.length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </List>
        ) : (
          <Box p={3} textAlign="center">
            <Typography variant="body1" gutterBottom>
              No products found
            </Typography>
          </Box>
        )}
      </Paper>
      
      {/* Highest Priced Products */}
      <Paper variant="outlined">
        <Box p={2}>
          <Typography variant="h6">Premium Products</Typography>
        </Box>
        <Divider />
        
        {productStats.highestPricedProducts.length > 0 ? (
          <List disablePadding>
            {productStats.highestPricedProducts.map((product, index) => (
              <React.Fragment key={product.id}>
                <ListItem 
                  button 
                  onClick={() => navigate(`/products/${product.id}`)}
                  sx={{ px: 2, py: 1.5 }}
                >
                  <ListItemText
                    primary={product.name}
                    secondary={`SKU: ${product.sku}`}
                  />
                  <Box sx={{ textAlign: 'right', minWidth: 120 }}>
                    <Typography variant="body1" color="primary" sx={{ fontWeight: 'bold' }}>
                      Rp {product.price?.toLocaleString()}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Stock: {product.stock}
                    </Typography>
                  </Box>
                </ListItem>
                {index < productStats.highestPricedProducts.length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </List>
        ) : (
          <Box p={3} textAlign="center">
            <Typography variant="body1" gutterBottom>
              No products found
            </Typography>
          </Box>
        )}
      </Paper>
    </Box>
  );
};

export default HomePage;