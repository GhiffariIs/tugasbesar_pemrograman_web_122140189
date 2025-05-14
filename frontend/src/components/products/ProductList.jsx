import { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Button,
  TextField,
  InputAdornment,
  IconButton,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Chip,
  Tooltip,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
  Alert,
  Grid
} from '@mui/material';
import {
  Add as AddIcon,
  Search as SearchIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  FilterList as FilterListIcon
} from '@mui/icons-material';
import { productService, categoryService } from '../../services/services';
import { formatCurrency } from '../../utils/formatters';
import ProductForm from './ProductForm';

const ProductList = () => {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  // Pagination & Filtering
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [totalProducts, setTotalProducts] = useState(0);
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState({
    category: '',
    stockStatus: ''
  });
  
  // Dialog states
  const [openAddDialog, setOpenAddDialog] = useState(false);
  const [openEditDialog, setOpenEditDialog] = useState(false);
  const [openDeleteDialog, setOpenDeleteDialog] = useState(false);
  const [currentProduct, setCurrentProduct] = useState(null);
  const [showFilters, setShowFilters] = useState(false);
  
  useEffect(() => {
    fetchCategories();
    fetchProducts();
  }, [page, rowsPerPage, searchQuery, filters]);
  
  const fetchCategories = async () => {
    try {
      // In a real app, this would be:
      // const response = await categoryService.getAllCategories();
      // setCategories(response.data);
      
      // For demo purposes
      setCategories([
        { id: 1, name: 'Laptop' },
        { id: 2, name: 'Aksesoris' },
        { id: 3, name: 'Monitor' },
        { id: 4, name: 'Audio' },
        { id: 5, name: 'Storage' }
      ]);
    } catch (error) {
      console.error('Error fetching categories:', error);
      setError('Gagal memuat data kategori');
    }
  };
  
  const fetchProducts = async () => {
    setLoading(true);
    setError('');
    
    try {
      // In a real app, this would be:
      // const params = {
      //   page,
      //   limit: rowsPerPage,
      //   search: searchQuery,
      //   ...filters
      // };
      // const response = await productService.getAllProducts(params);
      // setProducts(response.data.products);
      // setTotalProducts(response.data.total);
      
      // For demo purposes
      const demoProducts = [
        { id: 1, name: 'Laptop Asus ROG', sku: 'PRD-1234', price: 15000000, stock: 10, minStock: 5, category: { id: 1, name: 'Laptop' } },
        { id: 2, name: 'Mouse Wireless Logitech', sku: 'PRD-2345', price: 350000, stock: 3, minStock: 10, category: { id: 2, name: 'Aksesoris' } },
        { id: 3, name: 'Monitor LG 24inch', sku: 'PRD-3456', price: 2500000, stock: 8, minStock: 5, category: { id: 3, name: 'Monitor' } },
        { id: 4, name: 'Keyboard Mechanical', sku: 'PRD-4567', price: 1200000, stock: 15, minStock: 5, category: { id: 2, name: 'Aksesoris' } },
        { id: 5, name: 'Headphone Sony', sku: 'PRD-5678', price: 1800000, stock: 5, minStock: 5, category: { id: 4, name: 'Audio' } },
        { id: 6, name: 'SSD Samsung 1TB', sku: 'PRD-6789', price: 1500000, stock: 12, minStock: 5, category: { id: 5, name: 'Storage' } },
        { id: 7, name: 'Webcam Logitech', sku: 'PRD-7890', price: 950000, stock: 7, minStock: 5, category: { id: 2, name: 'Aksesoris' } },
        { id: 8, name: 'Router Wifi TP-Link', sku: 'PRD-8901', price: 450000, stock: 9, minStock: 5, category: { id: 2, name: 'Aksesoris' } },
        { id: 9, name: 'Monitor Samsung 27inch', sku: 'PRD-9012', price: 3200000, stock: 6, minStock: 5, category: { id: 3, name: 'Monitor' } },
        { id: 10, name: 'Laptop HP Pavilion', sku: 'PRD-0123', price: 9500000, stock: 4, minStock: 5, category: { id: 1, name: 'Laptop' } },
      ];
      
      // Apply frontend filtering for demo
      let filteredProducts = [...demoProducts];
      
      if (searchQuery) {
        filteredProducts = filteredProducts.filter(product => 
          product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
          product.sku.toLowerCase().includes(searchQuery.toLowerCase())
        );
      }
      
      if (filters.category) {
        filteredProducts = filteredProducts.filter(product => 
          product.category.id === parseInt(filters.category)
        );
      }
      
      if (filters.stockStatus === 'low') {
        filteredProducts = filteredProducts.filter(product => 
          product.stock < product.minStock
        );
      } else if (filters.stockStatus === 'out') {
        filteredProducts = filteredProducts.filter(product => 
          product.stock === 0
        );
      }
      
      setTotalProducts(filteredProducts.length);
      
      // Apply pagination for demo
      const startIndex = page * rowsPerPage;
      const paginatedProducts = filteredProducts.slice(startIndex, startIndex + rowsPerPage);
      
      setProducts(paginatedProducts);
    } catch (error) {
      console.error('Error fetching products:', error);
      setError('Gagal memuat data produk');
    } finally {
      setLoading(false);
    }
  };
  
  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };
  
  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value);
    setPage(0); // Reset to first page when searching
  };
  
  const handleFilterChange = (event) => {
    const { name, value } = event.target;
    setFilters(prev => ({
      ...prev,
      [name]: value
    }));
    setPage(0); // Reset to first page when filtering
  };
  
  const handleAddProduct = () => {
    setCurrentProduct(null);
    setOpenAddDialog(true);
  };
  
  const handleEditProduct = (product) => {
    setCurrentProduct(product);
    setOpenEditDialog(true);
  };
  
  const handleDeleteClick = (product) => {
    setCurrentProduct(product);
    setOpenDeleteDialog(true);
  };
  
  const handleSaveProduct = async (productData) => {
    setLoading(true);
    setError('');
    setSuccess('');
    
    try {
      if (!currentProduct) {
        // Create new product
        // In a real app: await productService.createProduct(productData);
        setSuccess('Produk berhasil ditambahkan!');
      } else {
        // Update existing product
        // In a real app: await productService.updateProduct(currentProduct.id, productData);
        setSuccess('Produk berhasil diperbarui!');
      }
      
      setOpenAddDialog(false);
      setOpenEditDialog(false);
      fetchProducts(); // Refresh the list
    } catch (error) {
      console.error('Error saving product:', error);
      setError('Gagal menyimpan produk. Silakan coba lagi.');
    } finally {
      setLoading(false);
    }
  };
  
  const handleConfirmDelete = async () => {
    setLoading(true);
    setError('');
    
    try {
      // In a real app: await productService.deleteProduct(currentProduct.id);
      setOpenDeleteDialog(false);
      setSuccess('Produk berhasil dihapus!');
      fetchProducts(); // Refresh the list
    } catch (error) {
      console.error('Error deleting product:', error);
      setError('Gagal menghapus produk. Silakan coba lagi.');
    } finally {
      setLoading(false);
    }
  };
  
  const getStockStatusChip = (product) => {
    if (product.stock === 0) {
      return <Chip size="small" label="Habis" color="error" icon={<WarningIcon />} />;
    } else if (product.stock < product.minStock) {
      return <Chip size="small" label="Stok Rendah" color="warning" icon={<WarningIcon />} />;
    } else {
      return <Chip size="small" label="Tersedia" color="success" icon={<CheckCircleIcon />} />;
    }
  };
  
  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1" gutterBottom>
          Daftar Produk
        </Typography>
        
        <Button
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
          onClick={handleAddProduct}
        >
          Tambah Produk
        </Button>
      </Box>
      
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}
      
      {success && (
        <Alert severity="success" sx={{ mb: 2 }}>
          {success}
        </Alert>
      )}
      
      <Paper elevation={2}>
        <Box p={2}>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} sm={6} md={4}>
              <TextField
                fullWidth
                id="search"
                placeholder="Cari produk..."
                variant="outlined"
                size="small"
                value={searchQuery}
                onChange={handleSearchChange}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <SearchIcon />
                    </InputAdornment>
                  ),
                }}
              />
            </Grid>
            
            <Grid item xs={10} sm={5} md={7}>
              {showFilters && (
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <FormControl fullWidth size="small">
                      <InputLabel id="category-filter-label">Kategori</InputLabel>
                      <Select
                        labelId="category-filter-label"
                        id="category-filter"
                        name="category"
                        value={filters.category}
                        label="Kategori"
                        onChange={handleFilterChange}
                      >
                        <MenuItem value="">Semua</MenuItem>
                        {categories.map(category => (
                          <MenuItem key={category.id} value={category.id}>
                            {category.name}
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <FormControl fullWidth size="small">
                      <InputLabel id="stock-filter-label">Status Stok</InputLabel>
                      <Select
                        labelId="stock-filter-label"
                        id="stock-filter"
                        name="stockStatus"
                        value={filters.stockStatus}
                        label="Status Stok"
                        onChange={handleFilterChange}
                      >
                        <MenuItem value="">Semua</MenuItem>
                        <MenuItem value="low">Stok Rendah</MenuItem>
                        <MenuItem value="out">Habis</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                </Grid>
              )}
            </Grid>
            
            <Grid item xs={2} sm={1} md={1} textAlign="right">
              <Tooltip title="Filter">
                <IconButton color={showFilters ? "primary" : "default"} onClick={() => setShowFilters(!showFilters)}>
                  <FilterListIcon />
                </IconButton>
              </Tooltip>
            </Grid>
          </Grid>
        </Box>
        
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>SKU</TableCell>
                <TableCell>Nama Produk</TableCell>
                <TableCell>Kategori</TableCell>
                <TableCell align="right">Harga</TableCell>
                <TableCell align="right">Stok</TableCell>
                <TableCell>Status</TableCell>
                <TableCell align="right">Aksi</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {loading ? (
                <TableRow>
                  <TableCell colSpan={7} align="center" sx={{ py: 3 }}>
                    <CircularProgress size={30} />
                    <Typography variant="body2" sx={{ mt: 1 }}>
                      Memuat data produk...
                    </Typography>
                  </TableCell>
                </TableRow>
              ) : products.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={7} align="center" sx={{ py: 3 }}>
                    <Typography variant="body1">
                      Tidak ada produk yang ditemukan
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {searchQuery ? "Coba ubah kata kunci pencarian" : "Tambahkan produk baru untuk memulai"}
                    </Typography>
                  </TableCell>
                </TableRow>
              ) : (
                products.map((product) => (
                  <TableRow key={product.id} hover>
                    <TableCell>{product.sku}</TableCell>
                    <TableCell>{product.name}</TableCell>
                    <TableCell>{product.category.name}</TableCell>
                    <TableCell align="right">{formatCurrency(product.price)}</TableCell>
                    <TableCell align="right">{product.stock}</TableCell>
                    <TableCell>{getStockStatusChip(product)}</TableCell>
                    <TableCell align="right">
                      <Tooltip title="Edit">
                        <IconButton
                          size="small"
                          color="primary"
                          onClick={() => handleEditProduct(product)}
                        >
                          <EditIcon fontSize="small" />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Hapus">
                        <IconButton
                          size="small"
                          color="error"
                          onClick={() => handleDeleteClick(product)}
                        >
                          <DeleteIcon fontSize="small" />
                        </IconButton>
                      </Tooltip>
                    </TableCell>
                  </TableRow>
                ))
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
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
          labelRowsPerPage="Baris per halaman:"
        />
      </Paper>
      
      {/* Add Product Dialog */}
      <Dialog 
        open={openAddDialog} 
        onClose={() => setOpenAddDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Tambah Produk</DialogTitle>
        <DialogContent dividers>
          <ProductForm 
            categories={categories} 
            onSave={handleSaveProduct} 
            loading={loading}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenAddDialog(false)}>
            Batal
          </Button>
        </DialogActions>
      </Dialog>
      
      {/* Edit Product Dialog */}
      <Dialog 
        open={openEditDialog} 
        onClose={() => setOpenEditDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Edit Produk</DialogTitle>
        <DialogContent dividers>
          <ProductForm 
            product={currentProduct}
            categories={categories} 
            onSave={handleSaveProduct} 
            loading={loading}
            isEdit
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenEditDialog(false)}>
            Batal
          </Button>
        </DialogActions>
      </Dialog>
      
      {/* Delete Confirmation Dialog */}
      <Dialog 
        open={openDeleteDialog}
        onClose={() => setOpenDeleteDialog(false)}
      >
        <DialogTitle>
          Konfirmasi Hapus Produk
        </DialogTitle>
        <DialogContent>
          <DialogContentText>
            Apakah Anda yakin ingin menghapus produk "{currentProduct?.name}"? 
            Tindakan ini tidak dapat dibatalkan.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button 
            onClick={() => setOpenDeleteDialog(false)}
            color="primary"
          >
            Batal
          </Button>
          <Button 
            onClick={handleConfirmDelete} 
            color="error" 
            variant="contained" 
            disabled={loading}
          >
            {loading ? <CircularProgress size={24} /> : 'Hapus'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ProductList;
