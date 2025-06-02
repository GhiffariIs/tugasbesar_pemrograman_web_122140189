import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Button,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TableSortLabel,
  TablePagination,
  TextField,
  InputAdornment,
  Chip,
  IconButton,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  DialogContentText,
  CircularProgress,
  Snackbar,
  Alert,
  useTheme,
  useMediaQuery,
  Card,
  CardContent,
  Grid
} from '@mui/material';
import {
  Add as AddIcon,
  Search as SearchIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Visibility as VisibilityIcon,
  Check as CheckIcon,
  Warning as WarningIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { productService } from '../services/services';

const ProductsPage = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const navigate = useNavigate();

  // State variables
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [totalItems, setTotalItems] = useState(0);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('name');
  const [sortDirection, setSortDirection] = useState('asc');
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [productToDelete, setProductToDelete] = useState(null);

  // Fetch products on component mount and when filters change
  useEffect(() => {
    fetchProducts();
  }, [page, rowsPerPage, sortBy, sortDirection]);

  // Fetch products with search and filters
  const fetchProducts = async () => {
    setLoading(true);
    try {
      const params = {
        page: page + 1,
        per_page: rowsPerPage,
        sort: sortBy,
        order: sortDirection,
        search: searchTerm
      };

      const response = await productService.getAllProducts(params);
      
      let fetchedProducts = [];
      let total = 0;
      
      // Handle different API response structures
      if (Array.isArray(response)) {
        fetchedProducts = response;
        total = response.length;
      } else if (response?.products && Array.isArray(response.products)) {
        fetchedProducts = response.products;
        total = response.pagination?.total_items || fetchedProducts.length;
      } else if (response?.data && Array.isArray(response.data)) {
        fetchedProducts = response.data;
        total = response.meta?.total || fetchedProducts.length;
      }
      
      setProducts(fetchedProducts);
      setTotalItems(total);
      setError('');
    } catch (err) {
      console.error('Error fetching products:', err);
      setError('Failed to load products. Please try again.');
      setProducts([]);
    } finally {
      setLoading(false);
    }
  };

  // Search handler
  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
    if (event.key === 'Enter') {
      setPage(0);
      fetchProducts();
    }
  };

  // Search button click
  const handleSearchClick = () => {
    setPage(0);
    fetchProducts();
  };

  // Sort handler
  const handleSort = (field) => {
    const isAsc = sortBy === field && sortDirection === 'asc';
    setSortDirection(isAsc ? 'desc' : 'asc');
    setSortBy(field);
  };

  // Pagination handlers
  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  // Delete handlers
  const openDeleteDialog = (product) => {
    setProductToDelete(product);
    setDeleteDialogOpen(true);
  };

  const closeDeleteDialog = () => {
    setDeleteDialogOpen(false);
    setProductToDelete(null);
  };

  const confirmDelete = async () => {
    if (!productToDelete) return;
    
    setLoading(true);
    try {
      await productService.deleteProduct(productToDelete.id);
      setProducts(products.filter(p => p.id !== productToDelete.id));
      setSuccessMessage(`Product "${productToDelete.name}" successfully deleted`);
      closeDeleteDialog();
      fetchProducts(); // Refresh the list
    } catch (err) {
      console.error('Error deleting product:', err);
      setError('Failed to delete product. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Navigation handlers
  const handleAddProduct = () => {
    navigate('/products/create');
  };

  const handleEditProduct = (id) => {
    navigate(`/products/${id}/edit`);
  };

  const handleViewProduct = (id) => {
    navigate(`/products/${id}`);
  };

  // Status chip for product stock
  const getStockStatusChip = (product) => {
    const minStock = product.minStock || 10;
    
    if (product.stock === 0) {
      return <Chip
        size="small" 
        color="error" 
        icon={<WarningIcon />} 
        label="Out of stock" 
      />;
    } else if (product.stock <= minStock) {
      return <Chip 
        size="small" 
        color="warning" 
        icon={<WarningIcon />} 
        label="Low stock" 
      />;
    } else {
      return <Chip 
        size="small" 
        color="success" 
        icon={<CheckIcon />} 
        label="In stock" 
      />;
    }
  };

  return (
    <Box>
      {/* Page header */}
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1">
          Products
        </Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
          onClick={handleAddProduct}
          sx={{ display: { xs: 'none', sm: 'flex' } }}
        >
          Add Product
        </Button>
      </Box>

      {/* Search and filter bar */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              variant="outlined"
              placeholder="Search products..."
              value={searchTerm}
              onChange={handleSearch}
              onKeyPress={(e) => e.key === 'Enter' && handleSearchClick()}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon />
                  </InputAdornment>
                ),
                endAdornment: searchTerm && (
                  <InputAdornment position="end">
                    <IconButton onClick={() => {
                      setSearchTerm('');
                      fetchProducts();
                    }} size="small">
                      ×
                    </IconButton>
                  </InputAdornment>
                ),
              }}
              size="small"
            />
          </Grid>
          <Grid item xs={12} sm={6} sx={{ textAlign: { xs: 'left', sm: 'right' } }}>
            <Button 
              variant="outlined" 
              onClick={handleSearchClick}
              startIcon={<SearchIcon />}
            >
              Search
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {/* Desktop View: Products Table */}
      {!isMobile && (
        <TableContainer component={Paper}>
          <Table size="medium">
            <TableHead>
              <TableRow>
                <TableCell>
                  <TableSortLabel
                    active={sortBy === 'name'}
                    direction={sortBy === 'name' ? sortDirection : 'asc'}
                    onClick={() => handleSort('name')}
                  >
                    Product Name
                  </TableSortLabel>
                </TableCell>
                <TableCell>SKU</TableCell>
                <TableCell>
                  <TableSortLabel
                    active={sortBy === 'price'}
                    direction={sortBy === 'price' ? sortDirection : 'asc'}
                    onClick={() => handleSort('price')}
                  >
                    Price
                  </TableSortLabel>
                </TableCell>
                <TableCell>
                  <TableSortLabel
                    active={sortBy === 'stock'}
                    direction={sortBy === 'stock' ? sortDirection : 'asc'}
                    onClick={() => handleSort('stock')}
                  >
                    Stock
                  </TableSortLabel>
                </TableCell>
                <TableCell align="center">Status</TableCell>
                <TableCell align="center">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {loading && page === 0 ? (
                <TableRow>
                  <TableCell colSpan={6} align="center" sx={{ py: 3 }}>
                    <CircularProgress size={40} />
                  </TableCell>
                </TableRow>
              ) : products.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={6} align="center" sx={{ py: 3 }}>
                    <Typography variant="body1">
                      No products found.
                    </Typography>
                    <Button 
                      variant="text" 
                      startIcon={<AddIcon />}
                      onClick={handleAddProduct}
                      sx={{ mt: 1 }}
                    >
                      Add a new product
                    </Button>
                  </TableCell>
                </TableRow>
              ) : (
                products.map((product) => (
                  <TableRow 
                    key={product.id}
                    hover
                    sx={{ cursor: 'pointer' }}
                    onClick={() => handleViewProduct(product.id)}
                  >
                    <TableCell component="th" scope="row">
                      {product.name}
                    </TableCell>
                    <TableCell>{product.id ? `PRD-${product.id}` : 'N/A'}</TableCell>
                    <TableCell>
                      Rp {(product.price || 0).toLocaleString()}
                    </TableCell>
                    <TableCell>{product.stock}</TableCell>
                    <TableCell align="center">
                      {getStockStatusChip(product)}
                    </TableCell>
                    <TableCell align="center" onClick={(e) => e.stopPropagation()}>
                      <IconButton 
                        size="small" 
                        onClick={(e) => {
                          e.stopPropagation();
                          handleViewProduct(product.id);
                        }}
                        sx={{ mr: 1 }}
                      >
                        <VisibilityIcon fontSize="small" />
                      </IconButton>
                      <IconButton 
                        size="small"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleEditProduct(product.id);
                        }}
                        sx={{ mr: 1 }}
                      >
                        <EditIcon fontSize="small" />
                      </IconButton>
                      <IconButton 
                        size="small"
                        color="error"
                        onClick={(e) => {
                          e.stopPropagation();
                          openDeleteDialog(product);
                        }}
                      >
                        <DeleteIcon fontSize="small" />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
          <TablePagination
            rowsPerPageOptions={[5, 10, 25, 50]}
            component="div"
            count={totalItems}
            rowsPerPage={rowsPerPage}
            page={page}
            onPageChange={handleChangePage}
            onRowsPerPageChange={handleChangeRowsPerPage}
          />
        </TableContainer>
      )}

      {/* Mobile View: Product Cards */}
      {isMobile && (
        <Box>
          {loading && page === 0 ? (
            <Box display="flex" justifyContent="center" my={4}>
              <CircularProgress />
            </Box>
          ) : products.length === 0 ? (
            <Box textAlign="center" my={4}>
              <Typography variant="body1" gutterBottom>
                No products found.
              </Typography>
              <Button 
                variant="contained" 
                startIcon={<AddIcon />}
                onClick={handleAddProduct}
                sx={{ mt: 1 }}
              >
                Add a new product
              </Button>
            </Box>
          ) : (
            <>
              {products.map((product) => (
                <Card 
                  key={product.id} 
                  sx={{ mb: 2, cursor: 'pointer' }}
                  onClick={() => handleViewProduct(product.id)}
                >
                  <CardContent>
                    <Box 
                      display="flex" 
                      justifyContent="space-between"
                      alignItems="flex-start"
                    >
                      <Box>
                        <Typography variant="h6" component="h2">
                          {product.name}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          SKU: {product.id ? `PRD-${product.id}` : 'N/A'}
                        </Typography>
                      </Box>
                      {getStockStatusChip(product)}
                    </Box>
                    
                    <Grid container spacing={2} sx={{ mt: 1 }}>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">
                          Price
                        </Typography>
                        <Typography variant="body1" fontWeight="bold">
                          Rp {(product.price || 0).toLocaleString()}
                        </Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">
                          Stock
                        </Typography>
                        <Typography variant="body1">
                          {product.stock} units
                        </Typography>
                      </Grid>
                    </Grid>
                    
                    <Box 
                      display="flex" 
                      justifyContent="flex-end" 
                      mt={2}
                      onClick={(e) => e.stopPropagation()}
                    >
                      <IconButton 
                        size="small" 
                        onClick={(e) => {
                          e.stopPropagation();
                          handleEditProduct(product.id);
                        }}
                        sx={{ mr: 1 }}
                      >
                        <EditIcon fontSize="small" />
                      </IconButton>
                      <IconButton 
                        size="small"
                        color="error"
                        onClick={(e) => {
                          e.stopPropagation();
                          openDeleteDialog(product);
                        }}
                      >
                        <DeleteIcon fontSize="small" />
                      </IconButton>
                    </Box>
                  </CardContent>
                </Card>
              ))}
              
              <Box display="flex" justifyContent="center" mt={2}>
                <TablePagination
                  component="div"
                  count={totalItems}
                  page={page}
                  onPageChange={handleChangePage}
                  rowsPerPage={rowsPerPage}
                  onRowsPerPageChange={handleChangeRowsPerPage}
                  rowsPerPageOptions={[5, 10, 25]}
                  labelRowsPerPage=""
                />
              </Box>
            </>
          )}
          
          {/* Floating action button for mobile */}
          <Box
            position="fixed"
            bottom={16}
            right={16}
            zIndex={theme.zIndex.fab}
          >
            <Button
              variant="contained"
              color="primary"
              sx={{ width: 56, height: 56, borderRadius: '50%' }}
              onClick={handleAddProduct}
            >
              <AddIcon />
            </Button>
          </Box>
        </Box>
      )}

      {/* Delete Confirmation Dialog */}
      <Dialog
        open={deleteDialogOpen}
        onClose={closeDeleteDialog}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">
          Confirm Delete
        </DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            Are you sure you want to delete the product "{productToDelete?.name}"? This action cannot be undone.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={closeDeleteDialog}>Cancel</Button>
          <Button onClick={confirmDelete} color="error" variant="contained" autoFocus>
            Delete
          </Button>
        </DialogActions>
      </Dialog>

      {/* Success message */}
      <Snackbar
        open={!!successMessage}
        autoHideDuration={6000}
        onClose={() => setSuccessMessage('')}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert 
          onClose={() => setSuccessMessage('')} 
          severity="success"
          variant="filled"
        >
          {successMessage}
        </Alert>
      </Snackbar>

      {/* Error message */}
      <Snackbar
        open={!!error}
        autoHideDuration={6000}
        onClose={() => setError('')}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert 
          onClose={() => setError('')} 
          severity="error"
          variant="filled"
        >
          {error}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default ProductsPage;