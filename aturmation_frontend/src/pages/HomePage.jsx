import React, { useState, useEffect } from 'react';
import { 
  Box, Typography, Paper, Grid, Card, CardContent, 
  Divider, LinearProgress
} from '@mui/material';
import { Inventory as InventoryIcon } from '@mui/icons-material';
import { productService } from '../services/services';

const HomePage = () => {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalProducts: 0,
    lowStock: 0
  });
  
  useEffect(() => {
    const fetchStats = async () => {
      setLoading(true);
      try {
        const productsResponse = await productService.getAllProducts({});
        
        // Extract data from response based on its structure
        const products = Array.isArray(productsResponse) 
          ? productsResponse 
          : (productsResponse.products || []);
          
        // Calculate stats
        const totalProducts = products.length;
        const lowStock = products.filter(p => (p.stock || 0) < 10).length;
        
        setStats({
          totalProducts,
          lowStock
        });
        
      } catch (error) {
        console.error('Error fetching data for homepage:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchStats();
  }, []);
  
  if (loading) {
    return <LinearProgress />;
  }
  
  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Welcome to Aturmation
      </Typography>
      
      <Typography variant="body1" paragraph>
        Manage your inventory efficiently with our simple, user-friendly system.
      </Typography>
      
      <Divider sx={{ my: 3 }} />
      
      <Typography variant="h5" gutterBottom>
        System Overview
      </Typography>
      
      <Grid container spacing={3} mt={1}>
        <Grid xs={12} sm={6} lg={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <InventoryIcon sx={{ fontSize: 40, color: 'primary.main', mr: 2 }} />
                <Box>
                  <Typography color="textSecondary" variant="subtitle2">
                    Total Products
                  </Typography>
                  <Typography variant="h4">
                    {stats.totalProducts}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid xs={12} sm={6} lg={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <InventoryIcon sx={{ fontSize: 40, color: 'warning.main', mr: 2 }} />
                <Box>
                  <Typography color="textSecondary" variant="subtitle2">
                    Low Stock Items
                  </Typography>
                  <Typography variant="h4">
                    {stats.lowStock}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
      
      <Paper sx={{ p: 3, mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          Getting Started
        </Typography>
        
        <Typography variant="body2" paragraph>
          1. Use the <strong>Products</strong> section to manage your inventory.
        </Typography>
        
        <Typography variant="body2" paragraph>
          2. Administrators can manage system users in the <strong>Users</strong> section.
        </Typography>
        
        <Typography variant="body2" paragraph>
          3. Update your profile and preferences in the <strong>Settings</strong> section.
        </Typography>
      </Paper>
    </Box>
  );
};

export default HomePage;