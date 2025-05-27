import { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Tabs,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
  InputAdornment,
  Alert,
  CircularProgress,
  IconButton,
  Tooltip,
  Chip
} from '@mui/material';
import { 
  Add as AddIcon,
  TrendingUp as StockInIcon,
  TrendingDown as StockOutIcon,
  FilterList as FilterIcon,
  Search as SearchIcon,
  CalendarToday as CalendarIcon
} from '@mui/icons-material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { id } from 'date-fns/locale';
import { transactionService, productService } from '../../services/services';
import { formatDate, formatDateTime, formatCurrency } from '../../utils/formatters';

const TransactionList = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [transactions, setTransactions] = useState([]);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  // Pagination
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [totalTransactions, setTotalTransactions] = useState(0);
  
  // Filters
  const [filters, setFilters] = useState({
    startDate: null,
    endDate: null,
    productId: '',
    searchQuery: ''
  });
  const [showFilters, setShowFilters] = useState(false);
  
  // New transaction form
  const [openStockInDialog, setOpenStockInDialog] = useState(false);
  const [openStockOutDialog, setOpenStockOutDialog] = useState(false);
  const [transactionForm, setTransactionForm] = useState({
    productId: '',
    quantity: '',
    date: new Date(),
    notes: ''
  });
  
  useEffect(() => {
    fetchProducts();
    fetchTransactions();
  }, [activeTab, page, rowsPerPage]);
  
  const fetchProducts = async () => {
    try {
      // In a real app: const response = await productService.getAllProducts();
      // setProducts(response.data);
      
      // Mock data for demo
      setProducts([
        { id: 1, name: 'Laptop Asus ROG', sku: 'PRD-1234', price: 15000000, stock: 10, minStock: 5 },
        { id: 2, name: 'Mouse Wireless Logitech', sku: 'PRD-2345', price: 350000, stock: 3, minStock: 10 },
        { id: 3, name: 'Monitor LG 24inch', sku: 'PRD-3456', price: 2500000, stock: 8, minStock: 5 },
        { id: 4, name: 'Keyboard Mechanical', sku: 'PRD-4567', price: 1200000, stock: 15, minStock: 5 },
        { id: 5, name: 'Headphone Sony', sku: 'PRD-5678', price: 1800000, stock: 5, minStock: 5 },
      ]);
    } catch (error) {
      console.error('Error fetching products:', error);
    }
  };
  
  const fetchTransactions = async () => {
    setLoading(true);
    setError('');
    
    try {
      // In a real app:
      // const params = {
      //   page,
      //   limit: rowsPerPage,
      //   ...filters,
      //   type: activeTab === 0 ? undefined : activeTab === 1 ? 'in' : 'out'
      // };
      // const response = await transactionService.getAllTransactions(params);
      // setTransactions(response.data.transactions);
      // setTotalTransactions(response.data.total);
      
      // Mock data for demo
      const mockTransactions = [
        { 
          id: 1, 
          type: 'in', 
          product: { id: 1, name: 'Laptop Asus ROG', sku: 'PRD-1234' },
          quantity: 5, 
          date: '2025-05-14T09:30:00', 
          notes: 'Restock from supplier',
          createdBy: 'Admin'
        },
        { 
          id: 2, 
          type: 'out', 
          product: { id: 2, name: 'Mouse Wireless Logitech', sku: 'PRD-2345' },
          quantity: 3, 
          date: '2025-05-14T10:45:00', 
          notes: 'Customer order #A001',
          createdBy: 'Admin'
        },
        { 
          id: 3, 
          type: 'in', 
          product: { id: 3, name: 'Keyboard Mechanical', sku: 'PRD-4567' },
          quantity: 10, 
          date: '2025-05-13T14:20:00', 
          notes: 'New inventory',
          createdBy: 'Admin'
        },
        { 
          id: 4, 
          type: 'out', 
          product: { id: 4, name: 'Monitor LG 24inch', sku: 'PRD-3456' },
          quantity: 2, 
          date: '2025-05-13T16:05:00', 
          notes: 'Customer order #A002',
          createdBy: 'Admin'
        },
        { 
          id: 5, 
          type: 'out', 
          product: { id: 5, name: 'Headphone Sony', sku: 'PRD-5678' },
          quantity: 1, 
          date: '2025-05-12T11:30:00', 
          notes: 'Staff use',
          createdBy: 'Admin'
        },
        { 
          id: 6, 
          type: 'in', 
          product: { id: 2, name: 'Mouse Wireless Logitech', sku: 'PRD-2345' },
          quantity: 15, 
          date: '2025-05-12T09:15:00', 
          notes: 'New batch arrival',
          createdBy: 'Admin'
        },
        { 
          id: 7, 
          type: 'in', 
          product: { id: 5, name: 'Headphone Sony', sku: 'PRD-5678' },
          quantity: 8, 
          date: '2025-05-11T13:45:00', 
          notes: 'Initial stock',
          createdBy: 'Admin'
        },
      ];
      
      // Filter based on tab
      let filteredTransactions = [...mockTransactions];
      
      if (activeTab === 1) {
        filteredTransactions = filteredTransactions.filter(t => t.type === 'in');
      } else if (activeTab === 2) {
        filteredTransactions = filteredTransactions.filter(t => t.type === 'out');
      }
      
      // Apply other filters
      if (filters.productId) {
        filteredTransactions = filteredTransactions.filter(
          t => t.product.id === parseInt(filters.productId)
        );
      }
      
      if (filters.searchQuery) {
        const query = filters.searchQuery.toLowerCase();
        filteredTransactions = filteredTransactions.filter(
          t => t.product.name.toLowerCase().includes(query) || 
               t.product.sku.toLowerCase().includes(query) ||
               t.notes?.toLowerCase().includes(query)
        );
      }
      
      if (filters.startDate) {
        filteredTransactions = filteredTransactions.filter(
          t => new Date(t.date) >= filters.startDate
        );
      }
      
      if (filters.endDate) {
        // Add one day to include the end date fully
        const endDate = new Date(filters.endDate);
        endDate.setDate(endDate.getDate() + 1);
        
        filteredTransactions = filteredTransactions.filter(
          t => new Date(t.date) <= endDate
        );
      }
      
      // Sort by date, newest first
      filteredTransactions.sort((a, b) => new Date(b.date) - new Date(a.date));
      
      setTotalTransactions(filteredTransactions.length);
      
      // Apply pagination
      const startIndex = page * rowsPerPage;
      const paginatedTransactions = filteredTransactions.slice(startIndex, startIndex + rowsPerPage);
      
      setTransactions(paginatedTransactions);
    } catch (error) {
      console.error('Error fetching transactions:', error);
      setError('Gagal memuat data transaksi');
    } finally {
      setLoading(false);
    }
  };
  
  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
    setPage(0); // Reset to first page when changing tabs
  };
  
  const handleChangePage = (event, newValue) => {
    setPage(newValue);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };
  
  const handleFilterChange = (event) => {
    const { name, value } = event.target;
    setFilters(prev => ({
      ...prev,
      [name]: value
    }));
  };
  
  const handleDateChange = (name, date) => {
    setFilters(prev => ({
      ...prev,
      [name]: date
    }));
  };
  
  const handleOpenStockInDialog = () => {
    setTransactionForm({
      productId: '',
      quantity: '',
      date: new Date(),
      notes: ''
    });
    setOpenStockInDialog(true);
  };
  
  const handleOpenStockOutDialog = () => {
    setTransactionForm({
      productId: '',
      quantity: '',
      date: new Date(),
      notes: ''
    });
    setOpenStockOutDialog(true);
  };
  
  const handleTransactionFormChange = (event) => {
    const { name, value } = event.target;
    
    if (name === 'quantity') {
      // Only allow positive integers
      const numValue = parseInt(value, 10);
      if (isNaN(numValue) || numValue < 1) {
        setTransactionForm(prev => ({
          ...prev,
          [name]: ''
        }));
        return;
      }
    }
    
    setTransactionForm(prev => ({
      ...prev,
      [name]: value
    }));
  };
  
  const handleTransactionDateChange = (date) => {
    setTransactionForm(prev => ({
      ...prev,
      date
    }));
  };
  
  const handleSubmitTransaction = async (type) => {
    setLoading(true);
    setError('');
    
    try {
      // Validation
      if (!transactionForm.productId || !transactionForm.quantity) {
        setError('Produk dan jumlah wajib diisi');
        setLoading(false);
        return;
      }
      
      const selectedProduct = products.find(p => p.id === parseInt(transactionForm.productId));
      
      if (type === 'out' && parseInt(transactionForm.quantity) > selectedProduct.stock) {
        setError(`Stok ${selectedProduct.name} tidak cukup. Stok saat ini: ${selectedProduct.stock}`);
        setLoading(false);
        return;
      }
      
      // In a real app:
      // const transactionData = {
      //   productId: transactionForm.productId,
      //   quantity: parseInt(transactionForm.quantity),
      //   type,
      //   date: transactionForm.date,
      //   notes: transactionForm.notes
      // };
      // await transactionService.createTransaction(transactionData);
      
      // Close dialogs and refresh
      if (type === 'in') {
        setOpenStockInDialog(false);
        setSuccess('Transaksi barang masuk berhasil ditambahkan!');
      } else {
        setOpenStockOutDialog(false);
        setSuccess('Transaksi barang keluar berhasil ditambahkan!');
      }
      
      fetchTransactions();
      fetchProducts(); // To update stock counts
    } catch (error) {
      console.error('Error submitting transaction:', error);
      setError('Gagal menyimpan transaksi. Silakan coba lagi.');
    } finally {
      setLoading(false);
    }
  };
  
  const applyFilters = () => {
    setPage(0);
    fetchTransactions();
  };
  
  const clearFilters = () => {
    setFilters({
      startDate: null,
      endDate: null,
      productId: '',
      searchQuery: ''
    });
    setPage(0);
    fetchTransactions();
  };
  
  return (
    <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={id}>
      <Box>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
          <Typography variant="h4" component="h1" gutterBottom>
            Transaksi Barang
          </Typography>
          
          <Box>
            <Button
              variant="contained"
              color="success"
              startIcon={<StockInIcon />}
              onClick={handleOpenStockInDialog}
              sx={{ mr: 1 }}
            >
              Barang Masuk
            </Button>
            <Button
              variant="contained"
              color="error"
              startIcon={<StockOutIcon />}
              onClick={handleOpenStockOutDialog}
            >
              Barang Keluar
            </Button>
          </Box>
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
        
        <Paper elevation={2} sx={{ mb: 3 }}>
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs 
              value={activeTab} 
              onChange={handleTabChange}
              variant="fullWidth"
            >
              <Tab label="Semua Transaksi" />
              <Tab label="Barang Masuk" />
              <Tab label="Barang Keluar" />
            </Tabs>
          </Box>
          
          <Box p={2}>
            <Box display="flex" alignItems="center" justifyContent="space-between">
              <TextField
                placeholder="Cari transaksi..."
                variant="outlined"
                size="small"
                sx={{ width: 250 }}
                value={filters.searchQuery}
                onChange={(e) => setFilters(prev => ({ ...prev, searchQuery: e.target.value }))}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <SearchIcon />
                    </InputAdornment>
                  ),
                }}
              />
              
              <Box>
                <Button 
                  variant={showFilters ? "contained" : "outlined"}
                  startIcon={<FilterIcon />}
                  size="small"
                  onClick={() => setShowFilters(!showFilters)}
                >
                  Filter
                </Button>
              </Box>
            </Box>
            
            {showFilters && (
              <Box mt={2}>
                <Grid container spacing={2} alignItems="center">
                  <Grid item xs={12} md={3}>
                    <DatePicker
                      label="Dari Tanggal"
                      value={filters.startDate}
                      onChange={(date) => handleDateChange('startDate', date)}
                      slotProps={{ 
                        textField: { 
                          size: 'small', 
                          fullWidth: true,
                          InputProps: {
                            startAdornment: (
                              <InputAdornment position="start">
                                <CalendarIcon fontSize="small" />
                              </InputAdornment>
                            ),
                          }
                        } 
                      }}
                    />
                  </Grid>
                  <Grid item xs={12} md={3}>
                    <DatePicker
                      label="Sampai Tanggal"
                      value={filters.endDate}
                      onChange={(date) => handleDateChange('endDate', date)}
                      slotProps={{ 
                        textField: { 
                          size: 'small', 
                          fullWidth: true,
                          InputProps: {
                            startAdornment: (
                              <InputAdornment position="start">
                                <CalendarIcon fontSize="small" />
                              </InputAdornment>
                            ),
                          }
                        } 
                      }}
                    />
                  </Grid>
                  <Grid item xs={12} md={4}>
                    <FormControl fullWidth size="small">
                      <InputLabel id="product-filter-label">Produk</InputLabel>
                      <Select
                        labelId="product-filter-label"
                        id="productId"
                        name="productId"
                        value={filters.productId}
                        label="Produk"
                        onChange={handleFilterChange}
                      >
                        <MenuItem value="">Semua Produk</MenuItem>
                        {products.map((product) => (
                          <MenuItem key={product.id} value={product.id}>
                            {product.name}
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item xs={12} md={2}>
                    <Box display="flex" gap={1}>
                      <Button
                        variant="contained"
                        fullWidth
                        onClick={applyFilters}
                      >
                        Terapkan
                      </Button>
                      <Button
                        variant="outlined"
                        fullWidth
                        onClick={clearFilters}
                      >
                        Reset
                      </Button>
                    </Box>
                  </Grid>
                </Grid>
              </Box>
            )}
          </Box>
          
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Tanggal</TableCell>
                  <TableCell>Kode</TableCell>
                  <TableCell>Produk</TableCell>
                  <TableCell>Jenis</TableCell>
                  <TableCell align="right">Jumlah</TableCell>
                  <TableCell>Keterangan</TableCell>
                  <TableCell>Oleh</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {loading ? (
                  <TableRow>
                    <TableCell colSpan={7} align="center" sx={{ py: 3 }}>
                      <CircularProgress size={30} />
                      <Typography variant="body2" sx={{ mt: 1 }}>
                        Memuat data transaksi...
                      </Typography>
                    </TableCell>
                  </TableRow>
                ) : transactions.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={7} align="center" sx={{ py: 3 }}>
                      <Typography variant="body1">
                        Tidak ada data transaksi
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {filters.startDate || filters.endDate || filters.productId || filters.searchQuery ? 
                          "Coba ubah filter pencarian" : 
                          "Tambahkan transaksi baru untuk memulai"}
                      </Typography>
                    </TableCell>
                  </TableRow>
                ) : (
                  transactions.map((transaction) => (
                    <TableRow key={transaction.id} hover>
                      <TableCell>{formatDateTime(transaction.date)}</TableCell>
                      <TableCell>{transaction.product.sku}</TableCell>
                      <TableCell>{transaction.product.name}</TableCell>
                      <TableCell>
                        <Chip
                          label={transaction.type === 'in' ? "Masuk" : "Keluar"}
                          color={transaction.type === 'in' ? "success" : "error"}
                          size="small"
                          variant="outlined"
                        />
                      </TableCell>
                      <TableCell align="right">
                        <Typography
                          component="span"
                          sx={{
                            color: transaction.type === 'in' ? 'success.main' : 'error.main',
                            fontWeight: 'medium'
                          }}
                        >
                          {transaction.type === 'in' ? '+' : '-'}{transaction.quantity}
                        </Typography>
                      </TableCell>
                      <TableCell>{transaction.notes || '-'}</TableCell>
                      <TableCell>{transaction.createdBy}</TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </TableContainer>
          
          <TablePagination
            rowsPerPageOptions={[5, 10, 25]}
            component="div"
            count={totalTransactions}
            rowsPerPage={rowsPerPage}
            page={page}
            onPageChange={handleChangePage}
            onRowsPerPageChange={handleChangeRowsPerPage}
            labelRowsPerPage="Baris per halaman:"
          />
        </Paper>
        
        {/* Stock In Dialog */}
        <Dialog 
          open={openStockInDialog} 
          onClose={() => setOpenStockInDialog(false)}
          maxWidth="sm"
          fullWidth
        >
          <DialogTitle>Tambah Barang Masuk</DialogTitle>
          <DialogContent dividers>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <FormControl fullWidth required>
                  <InputLabel id="product-label">Produk</InputLabel>
                  <Select
                    labelId="product-label"
                    id="productId"
                    name="productId"
                    value={transactionForm.productId}
                    label="Produk"
                    onChange={handleTransactionFormChange}
                  >
                    {products.map((product) => (
                      <MenuItem key={product.id} value={product.id}>
                        {product.name} ({product.sku})
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  required
                  id="quantity"
                  name="quantity"
                  label="Jumlah"
                  type="number"
                  value={transactionForm.quantity}
                  onChange={handleTransactionFormChange}
                  InputProps={{ inputProps: { min: 1 } }}
                />
              </Grid>
              
              <Grid item xs={12}>
                <DatePicker
                  label="Tanggal"
                  value={transactionForm.date}
                  onChange={handleTransactionDateChange}
                  slotProps={{ textField: { fullWidth: true } }}
                />
              </Grid>
              
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  id="notes"
                  name="notes"
                  label="Keterangan"
                  value={transactionForm.notes}
                  onChange={handleTransactionFormChange}
                  multiline
                  rows={3}
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenStockInDialog(false)}>
              Batal
            </Button>
            <Button 
              onClick={() => handleSubmitTransaction('in')} 
              variant="contained" 
              color="success"
              disabled={loading}
            >
              {loading ? <CircularProgress size={24} /> : 'Simpan'}
            </Button>
          </DialogActions>
        </Dialog>
        
        {/* Stock Out Dialog */}
        <Dialog 
          open={openStockOutDialog} 
          onClose={() => setOpenStockOutDialog(false)}
          maxWidth="sm"
          fullWidth
        >
          <DialogTitle>Tambah Barang Keluar</DialogTitle>
          <DialogContent dividers>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <FormControl fullWidth required>
                  <InputLabel id="product-out-label">Produk</InputLabel>
                  <Select
                    labelId="product-out-label"
                    id="productId"
                    name="productId"
                    value={transactionForm.productId}
                    label="Produk"
                    onChange={handleTransactionFormChange}
                  >
                    {products.map((product) => (
                      <MenuItem 
                        key={product.id} 
                        value={product.id}
                        disabled={product.stock <= 0}
                      >
                        {product.name} ({product.sku}) - Stok: {product.stock}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  required
                  id="quantity"
                  name="quantity"
                  label="Jumlah"
                  type="number"
                  value={transactionForm.quantity}
                  onChange={handleTransactionFormChange}
                  InputProps={{ 
                    inputProps: { 
                      min: 1,
                      max: transactionForm.productId ? 
                        products.find(p => p.id === parseInt(transactionForm.productId))?.stock || 1 : 1
                    } 
                  }}
                  helperText={transactionForm.productId ? 
                    `Stok tersedia: ${products.find(p => p.id === parseInt(transactionForm.productId))?.stock || 0}` : ''}
                />
              </Grid>
              
              <Grid item xs={12}>
                <DatePicker
                  label="Tanggal"
                  value={transactionForm.date}
                  onChange={handleTransactionDateChange}
                  slotProps={{ textField: { fullWidth: true } }}
                />
              </Grid>
              
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  id="notes"
                  name="notes"
                  label="Keterangan"
                  value={transactionForm.notes}
                  onChange={handleTransactionFormChange}
                  multiline
                  rows={3}
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenStockOutDialog(false)}>
              Batal
            </Button>
            <Button 
              onClick={() => handleSubmitTransaction('out')} 
              variant="contained" 
              color="error"
              disabled={loading}
            >
              {loading ? <CircularProgress size={24} /> : 'Simpan'}
            </Button>
          </DialogActions>
        </Dialog>
      </Box>
    </LocalizationProvider>
  );
};

export default TransactionList;
