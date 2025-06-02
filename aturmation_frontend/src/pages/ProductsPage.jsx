import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Button,
  Dialog,
  DialogContent,
  DialogTitle,
  CircularProgress,
  Snackbar,
  Alert,
  useTheme,
  useMediaQuery,
  IconButton
} from '@mui/material';
import { Add as AddIcon, Close as CloseIcon } from '@mui/icons-material';
import { productService } from '../services/services';
import ProductList from '../components/products/ProductList';
import ProductForm from '../components/products/ProductForm';

const ProductsPage = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [totalProducts, setTotalProducts] = useState(0);
  
  const [openAddDialog, setOpenAddDialog] = useState(false);
  const [openEditDialog, setOpenEditDialog] = useState(false);
  const [currentProduct, setCurrentProduct] = useState(null);
  
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [filters, setFilters] = useState({
    search: '',
    sortBy: 'name',
    sortDir: 'asc',
  });
  
  const fetchProducts = async () => {
    setLoading(true);
    try {
      const params = {
        page: page + 1,
        per_page: rowsPerPage,
        search: filters.search,
        sort: filters.sortBy,
        order: filters.sortDir,
      };
      
      const response = await productService.getAllProducts(params);
      
      // Handle various response formats
      let fetchedProducts = [];
      let totalItems = 0;
      
      if (Array.isArray(response)) {
        fetchedProducts = response;
        totalItems = response.length;
      } 
      else if (response && Array.isArray(response.products)) {
        fetchedProducts = response.products;
        totalItems = response.pagination?.total_items || fetchedProducts.length;
      }
      else if (response && Array.isArray(response.data)) {
        fetchedProducts = response.data;
        totalItems = response.meta?.total || fetchedProducts.length;
      }
      
      setProducts(fetchedProducts);
      setTotalProducts(totalItems);
      setError('');
    } catch (error) {
      console.error('Error fetching products:', error);
      setError('Failed to load products');
      setProducts([]);
    } finally {
      setLoading(false);
    }
  };
  
  useEffect(() => {
    fetchProducts();
  }, [page, rowsPerPage, filters]);
  
  const handleSearchChange = (searchTerm) => {
    setFilters(prev => ({ ...prev, search: searchTerm }));
    // Only trigger immediate search if term is 3+ chars or empty
    if (searchTerm === '' || searchTerm.length >= 3) {
      setPage(0);
    }
  };
  
  const handleSortChange = (field) => {
    setFilters(prev => ({
      ...prev,
      sortBy: field,
      sortDir: prev.sortBy === field && prev.sortDir === 'asc' ? 'desc' : 'asc'
    }));
    setPage(0);
  };
  
  const handlePageChange = (event, newPage) => {
    setPage(newPage);
  };
  
  const handleRowsPerPageChange = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };
  
  const handleAddProduct = () => {
    setCurrentProduct(null);
    setOpenAddDialog(true);
  };
  
  const handleEditProduct = (id) => {
    const product = products.find(p => p.id === id);
    if (product) {
      setCurrentProduct(product);
      setOpenEditDialog(true);
    }
  };
  
  const handleDeleteProduct = async (id) => {
    try {
      await productService.deleteProduct(id);
      setSuccess('Product deleted successfully');
      fetchProducts();
    } catch (error) {
      console.error('Error deleting product:', error);
      setError('Failed to delete product');
    }
  };
  
  const handleSaveProduct = async (productData) => {
    setLoading(true);
    try {
      if (!currentProduct) {
        await productService.createProduct(productData);
        setSuccess('Product added successfully');
      } else {
        await productService.updateProduct(currentProduct.id, productData);
        setSuccess('Product updated successfully');
      }
      
      setOpenAddDialog(false);
      setOpenEditDialog(false);
      fetchProducts();
    } catch (error) {
      console.error('Error saving product:', error);
      setError('Failed to save product');
    } finally {
      setLoading(false);
    }
  };
  
  const handleCloseSnackbar = () => {
    setSuccess('');
    setError('');
  };
  
  return (
    <Box>
      <Snackbar 
        open={!!success} 
        autoHideDuration={6000} 
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert 
          onClose={handleCloseSnackbar} 
          severity="success"
          sx={{ width: '100%' }}
        >
          {success}
        </Alert>
      </Snackbar>
      
      <Snackbar 
        open={!!error && !loading} 
        autoHideDuration={6000} 
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert 
          onClose={handleCloseSnackbar} 
          severity="error"
          sx={{ width: '100%' }}
        >
          {error}
        </Alert>
      </Snackbar>
      
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Products</Typography>
        {!isMobile && (
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={handleAddProduct}
          >
            Add Product
          </Button>
        )}
      </Box>
      
      <ProductList
        products={products}
        loading={loading}
        error={error}
        totalProducts={totalProducts}
        page={page}
        rowsPerPage={rowsPerPage}
        onPageChange={handlePageChange}
        onRowsPerPageChange={handleRowsPerPageChange}
        onDelete={handleDeleteProduct}
        onSearch={handleSearchChange}
        onSort={handleSortChange}
        sortBy={filters.sortBy}
        sortDir={filters.sortDir}
        onAdd={handleAddProduct}
        onEdit={handleEditProduct}
      />
      
      {/* Add/Edit Product Dialog */}
      <Dialog
        open={openAddDialog || openEditDialog}
        onClose={() => openAddDialog ? setOpenAddDialog(false) : setOpenEditDialog(false)}
        maxWidth="md"
        fullWidth
        fullScreen={isMobile}
      >
        <DialogTitle sx={{ 
          m: 0, 
          p: 2, 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center' 
        }}>
          {openAddDialog ? 'Add New Product' : 'Edit Product'}
          <IconButton
            onClick={() => openAddDialog ? setOpenAddDialog(false) : setOpenEditDialog(false)}
            sx={{ color: 'grey.500' }}
          >
            <CloseIcon />
          </IconButton>
        </DialogTitle>
        <DialogContent dividers>
          <ProductForm
            product={currentProduct}
            onSave={handleSaveProduct}
            loading={loading}
            isEdit={!!currentProduct}
            onCancel={() => openAddDialog ? setOpenAddDialog(false) : setOpenEditDialog(false)}
          />
        </DialogContent>
      </Dialog>
    </Box>
  );
};

export default ProductsPage;