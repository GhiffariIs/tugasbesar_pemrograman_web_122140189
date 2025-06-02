import React, { useState, useEffect } from 'react';
import {
  Box,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TableSortLabel,
  IconButton,
  Chip,
  TextField,
  InputAdornment,
  CircularProgress,
  Typography,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Button,
  Paper,
  TablePagination,
  Tooltip,
  Card,
  Grid,
  useTheme,
  useMediaQuery
} from '@mui/material';
import {
  Delete as DeleteIcon,
  Edit as EditIcon,
  Search as SearchIcon,
  Visibility as VisibilityIcon,
  Add as AddIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const ProductList = ({
  products,
  loading,
  error,
  totalProducts,
  page,
  rowsPerPage,
  onPageChange,
  onRowsPerPageChange,
  onDelete,
  onSearch,
  onSort,
  sortBy,
  sortDir,
  onAdd,
  onEdit
}) => {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [productToDelete, setProductToDelete] = useState(null);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  const handleSearchChange = (e) => {
    const value = e.target.value;
    setSearchTerm(value);
    onSearch(value);
  };

  const handleView = (id) => {
    navigate(`/products/${id}`);
  };

  const handleEdit = (id) => {
    if (onEdit) {
      onEdit(id);
    } else {
      navigate(`/products/${id}`);
    }
  };

  const handleDeleteClick = (product) => {
    setProductToDelete(product);
    setDeleteDialogOpen(true);
  };

  const handleDeleteConfirm = () => {
    if (productToDelete) {
      onDelete(productToDelete.id);
      setDeleteDialogOpen(false);
      setProductToDelete(null);
    }
  };

  const getSortDirection = (field) => {
    return sortBy === field ? sortDir : 'asc';
  };

  const getStockStatus = (product) => {
    if (product.stock === 0) {
      return (
        <Chip
          label="Out of stock"
          color="error"
          size="small"
          icon={<WarningIcon />}
          sx={{ width: '100%' }}
        />
      );
    } else if (product.stock <= (product.minStock || 10)) {
      return (
        <Chip
          label="Low stock"
          color="warning"
          size="small"
          icon={<WarningIcon />}
          sx={{ width: '100%' }}
        />
      );
    } else {
      return (
        <Chip
          label="In stock"
          color="success"
          size="small"
          icon={<CheckCircleIcon />}
          sx={{ width: '100%' }}
        />
      );
    }
  };

  // Mobile card view component
  const ProductCard = ({ product }) => (
    <Card sx={{ mb: 2, position: 'relative' }}>
      <Box sx={{ p: 2 }}>
        <Typography variant="h6" noWrap title={product.name}>
          {product.name}
        </Typography>
        <Typography variant="caption" color="text.secondary" gutterBottom>
          SKU: {product.sku}
        </Typography>
        
        <Grid container spacing={1} sx={{ mt: 1 }}>
          <Grid item xs={6}>
            <Typography variant="body2" color="text.secondary">
              Price
            </Typography>
            <Typography variant="body1" fontWeight="bold">
              Rp {product.price?.toLocaleString() || 0}
            </Typography>
          </Grid>
          
          <Grid item xs={6}>
            <Typography variant="body2" color="text.secondary">
              Stock
            </Typography>
            <Typography variant="body1" fontWeight="bold">
              {product.stock || 0} units
            </Typography>
          </Grid>
          
          <Grid item xs={12} sx={{ mt: 1 }}>
            {getStockStatus(product)}
          </Grid>
        </Grid>
      </Box>
      
      <Box sx={{ 
        display: 'flex', 
        justifyContent: 'flex-end', 
        p: 1, 
        borderTop: '1px solid rgba(0,0,0,0.12)'
      }}>
        <Tooltip title="View details">
          <IconButton 
            size="small" 
            onClick={() => handleView(product.id)}
            sx={{ mr: 1 }}
          >
            <VisibilityIcon />
          </IconButton>
        </Tooltip>
        
        <Tooltip title="Edit">
          <IconButton 
            size="small" 
            onClick={() => handleEdit(product.id)}
            sx={{ mr: 1 }}
          >
            <EditIcon />
          </IconButton>
        </Tooltip>
        
        <Tooltip title="Delete">
          <IconButton 
            size="small" 
            color="error" 
            onClick={() => handleDeleteClick(product)}
          >
            <DeleteIcon />
          </IconButton>
        </Tooltip>
      </Box>
    </Card>
  );

  return (
    <Box>
      <Box mb={2} display="flex" alignItems="center">
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Search products..."
          value={searchTerm}
          onChange={handleSearchChange}
          size="small"
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            ),
          }}
        />
        {!isMobile && (
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={onAdd}
            sx={{ ml: 2, height: 40, whiteSpace: 'nowrap' }}
          >
            Add Product
          </Button>
        )}
      </Box>

      {error && (
        <Typography color="error" align="center" my={2}>
          {error}
        </Typography>
      )}

      {/* Display products for desktop */}
      {!isMobile && (
        <Paper sx={{ width: '100%', overflow: 'hidden' }}>
          <TableContainer sx={{ maxHeight: 440 }}>
            <Table stickyHeader>
              <TableHead>
                <TableRow>
                  <TableCell>
                    <TableSortLabel
                      active={sortBy === 'name'}
                      direction={getSortDirection('name')}
                      onClick={() => onSort('name')}
                    >
                      Name
                    </TableSortLabel>
                  </TableCell>
                  <TableCell>SKU</TableCell>
                  <TableCell>
                    <TableSortLabel
                      active={sortBy === 'price'}
                      direction={getSortDirection('price')}
                      onClick={() => onSort('price')}
                    >
                      Price
                    </TableSortLabel>
                  </TableCell>
                  <TableCell>
                    <TableSortLabel
                      active={sortBy === 'stock'}
                      direction={getSortDirection('stock')}
                      onClick={() => onSort('stock')}
                    >
                      Stock
                    </TableSortLabel>
                  </TableCell>
                  <TableCell align="center">Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {loading ? (
                  <TableRow>
                    <TableCell colSpan={5} align="center">
                      <CircularProgress size={30} />
                    </TableCell>
                  </TableRow>
                ) : products.length > 0 ? (
                  products.map((product) => (
                    <TableRow 
                      key={product.id}
                      hover
                      sx={{ '&:hover': { bgcolor: 'action.hover', cursor: 'pointer' } }}
                      onClick={() => handleView(product.id)}
                    >
                      <TableCell>{product.name}</TableCell>
                      <TableCell>{product.sku}</TableCell>
                      <TableCell>Rp {product.price?.toLocaleString()}</TableCell>
                      <TableCell>
                        <Box display="flex" alignItems="center">
                          {product.stock}
                          <Box sx={{ ml: 1 }}>
                            {getStockStatus(product)}
                          </Box>
                        </Box>
                      </TableCell>
                      <TableCell align="center" onClick={(e) => e.stopPropagation()}>
                        <Tooltip title="View details">
                          <IconButton
                            onClick={(e) => {
                              e.stopPropagation();
                              handleView(product.id);
                            }}
                            size="small"
                          >
                            <VisibilityIcon />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title="Edit">
                          <IconButton
                            onClick={(e) => {
                              e.stopPropagation();
                              handleEdit(product.id);
                            }}
                            size="small"
                          >
                            <EditIcon />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title="Delete">
                          <IconButton
                            onClick={(e) => {
                              e.stopPropagation();
                              handleDeleteClick(product);
                            }}
                            size="small"
                            color="error"
                          >
                            <DeleteIcon />
                          </IconButton>
                        </Tooltip>
                      </TableCell>
                    </TableRow>
                  ))
                ) : (
                  <TableRow>
                    <TableCell colSpan={5} align="center">
                      <Typography variant="body1" p={2}>
                        No products found
                      </Typography>
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </TableContainer>
          <TablePagination
            rowsPerPageOptions={[5, 10, 25]}
            component="div"
            count={totalProducts}
            rowsPerPage={rowsPerPage}
            page={page}
            onPageChange={onPageChange}
            onRowsPerPageChange={onRowsPerPageChange}
          />
        </Paper>
      )}

      {/* Display products for mobile */}
      {isMobile && (
        <Box>
          {loading ? (
            <Box display="flex" justifyContent="center" p={4}>
              <CircularProgress />
            </Box>
          ) : products.length > 0 ? (
            <>
              {products.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
              <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
                <TablePagination
                  rowsPerPageOptions={[5, 10, 25]}
                  component="div"
                  count={totalProducts}
                  rowsPerPage={rowsPerPage}
                  page={page}
                  onPageChange={onPageChange}
                  onRowsPerPageChange={onRowsPerPageChange}
                  labelRowsPerPage=""
                />
              </Box>
              <Box sx={{ position: 'fixed', bottom: 16, right: 16 }}>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={onAdd}
                  sx={{ borderRadius: '50%', width: 56, height: 56 }}
                >
                  <AddIcon />
                </Button>
              </Box>
            </>
          ) : (
            <Box textAlign="center" p={4}>
              <Typography variant="body1" gutterBottom>
                No products found
              </Typography>
              <Button
                variant="contained"
                startIcon={<AddIcon />}
                onClick={onAdd}
                sx={{ mt: 2 }}
              >
                Add Product
              </Button>
            </Box>
          )}
        </Box>
      )}

      {/* Delete Confirmation Dialog */}
      <Dialog
        open={deleteDialogOpen}
        onClose={() => setDeleteDialogOpen(false)}
      >
        <DialogTitle>Confirm Delete</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to delete the product "{productToDelete?.name}"? This action cannot be undone.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>Cancel</Button>
          <Button 
            onClick={handleDeleteConfirm} 
            color="error"
            variant="contained"
          >
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ProductList;
