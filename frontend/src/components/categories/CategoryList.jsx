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
  CircularProgress,
  Alert,
  Grid
} from '@mui/material';
import {
  Add as AddIcon,
  Search as SearchIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  CategoryOutlined as CategoryIcon
} from '@mui/icons-material';
import { categoryService } from '../../services/services';
import CategoryForm from './CategoryForm';

const CategoryList = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  // Pagination & Filtering
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [totalCategories, setTotalCategories] = useState(0);
  const [searchQuery, setSearchQuery] = useState('');
  
  // Dialog states
  const [openAddDialog, setOpenAddDialog] = useState(false);
  const [openEditDialog, setOpenEditDialog] = useState(false);
  const [openDeleteDialog, setOpenDeleteDialog] = useState(false);
  const [currentCategory, setCurrentCategory] = useState(null);
  
  useEffect(() => {
    fetchCategories();
  }, [page, rowsPerPage, searchQuery]);
  
  const fetchCategories = async () => {
    setLoading(true);
    setError('');
    
    try {
      // In a real app, this would be:
      // const params = {
      //   page,
      //   limit: rowsPerPage,
      //   search: searchQuery
      // };
      // const response = await categoryService.getAllCategories(params);
      // setCategories(response.data.categories);
      // setTotalCategories(response.data.total);
      
      // For demo purposes
      const demoCategories = [
        { id: 1, name: 'Laptop', description: 'Komputer portabel', productCount: 15 },
        { id: 2, name: 'Aksesoris', description: 'Perangkat tambahan', productCount: 32 },
        { id: 3, name: 'Monitor', description: 'Layar komputer', productCount: 8 },
        { id: 4, name: 'Audio', description: 'Peralatan audio', productCount: 12 },
        { id: 5, name: 'Storage', description: 'Media penyimpanan', productCount: 9 },
        { id: 6, name: 'Networking', description: 'Perangkat jaringan', productCount: 7 },
        { id: 7, name: 'Printer', description: 'Perangkat cetak', productCount: 5 },
        { id: 8, name: 'Gaming', description: 'Perangkat gaming', productCount: 20 },
      ];
      
      // Apply frontend filtering for demo
      let filteredCategories = [...demoCategories];
      
      if (searchQuery) {
        filteredCategories = filteredCategories.filter(category => 
          category.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
          category.description?.toLowerCase().includes(searchQuery.toLowerCase())
        );
      }
      
      setTotalCategories(filteredCategories.length);
      
      // Apply pagination for demo
      const startIndex = page * rowsPerPage;
      const paginatedCategories = filteredCategories.slice(startIndex, startIndex + rowsPerPage);
      
      setCategories(paginatedCategories);
    } catch (error) {
      console.error('Error fetching categories:', error);
      setError('Gagal memuat data kategori');
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
  
  const handleAddCategory = () => {
    setCurrentCategory(null);
    setOpenAddDialog(true);
  };
  
  const handleEditCategory = (category) => {
    setCurrentCategory(category);
    setOpenEditDialog(true);
  };
  
  const handleDeleteClick = (category) => {
    setCurrentCategory(category);
    setOpenDeleteDialog(true);
  };
  
  const handleSaveCategory = async (categoryData) => {
    setLoading(true);
    setError('');
    setSuccess('');
    
    try {
      if (!currentCategory) {
        // Create new category
        // In a real app: await categoryService.createCategory(categoryData);
        setSuccess('Kategori berhasil ditambahkan!');
      } else {
        // Update existing category
        // In a real app: await categoryService.updateCategory(currentCategory.id, categoryData);
        setSuccess('Kategori berhasil diperbarui!');
      }
      
      setOpenAddDialog(false);
      setOpenEditDialog(false);
      fetchCategories(); // Refresh the list
    } catch (error) {
      console.error('Error saving category:', error);
      setError('Gagal menyimpan kategori. Silakan coba lagi.');
    } finally {
      setLoading(false);
    }
  };
  
  const handleConfirmDelete = async () => {
    setLoading(true);
    setError('');
    
    try {
      // In a real app: await categoryService.deleteCategory(currentCategory.id);
      setOpenDeleteDialog(false);
      setSuccess('Kategori berhasil dihapus!');
      fetchCategories(); // Refresh the list
    } catch (error) {
      console.error('Error deleting category:', error);
      setError('Gagal menghapus kategori. Silakan coba lagi.');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1" gutterBottom>
          Daftar Kategori
        </Typography>
        
        <Button
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
          onClick={handleAddCategory}
        >
          Tambah Kategori
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
          <TextField
            fullWidth
            id="search"
            placeholder="Cari kategori..."
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
        </Box>
        
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Nama Kategori</TableCell>
                <TableCell>Deskripsi</TableCell>
                <TableCell align="right">Jumlah Produk</TableCell>
                <TableCell align="right">Aksi</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {loading ? (
                <TableRow>
                  <TableCell colSpan={4} align="center" sx={{ py: 3 }}>
                    <CircularProgress size={30} />
                    <Typography variant="body2" sx={{ mt: 1 }}>
                      Memuat data kategori...
                    </Typography>
                  </TableCell>
                </TableRow>
              ) : categories.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={4} align="center" sx={{ py: 3 }}>
                    <Typography variant="body1">
                      Tidak ada kategori yang ditemukan
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {searchQuery ? "Coba ubah kata kunci pencarian" : "Tambahkan kategori baru untuk memulai"}
                    </Typography>
                  </TableCell>
                </TableRow>
              ) : (
                categories.map((category) => (
                  <TableRow key={category.id} hover>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <CategoryIcon sx={{ mr: 1, color: 'primary.main' }} fontSize="small" />
                        {category.name}
                      </Box>
                    </TableCell>
                    <TableCell>{category.description || '-'}</TableCell>
                    <TableCell align="right">
                      <Chip
                        size="small"
                        label={`${category.productCount} produk`}
                        color={category.productCount > 0 ? "primary" : "default"}
                        variant={category.productCount > 0 ? "outlined" : "filled"}
                      />
                    </TableCell>
                    <TableCell align="right">
                      <Tooltip title="Edit">
                        <IconButton
                          size="small"
                          color="primary"
                          onClick={() => handleEditCategory(category)}
                        >
                          <EditIcon fontSize="small" />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Hapus">
                        <IconButton
                          size="small"
                          color="error"
                          onClick={() => handleDeleteClick(category)}
                          disabled={category.productCount > 0}
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
          count={totalCategories}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
          labelRowsPerPage="Baris per halaman:"
        />
      </Paper>
      
      {/* Add Category Dialog */}
      <Dialog 
        open={openAddDialog} 
        onClose={() => setOpenAddDialog(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Tambah Kategori</DialogTitle>
        <DialogContent dividers>
          <CategoryForm 
            onSave={handleSaveCategory} 
            loading={loading}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenAddDialog(false)}>
            Batal
          </Button>
        </DialogActions>
      </Dialog>
      
      {/* Edit Category Dialog */}
      <Dialog 
        open={openEditDialog} 
        onClose={() => setOpenEditDialog(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Edit Kategori</DialogTitle>
        <DialogContent dividers>
          <CategoryForm 
            category={currentCategory}
            onSave={handleSaveCategory} 
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
          Konfirmasi Hapus Kategori
        </DialogTitle>
        <DialogContent>
          <DialogContentText>
            Apakah Anda yakin ingin menghapus kategori "{currentCategory?.name}"? 
            {currentCategory?.productCount > 0 && (
              <strong> Kategori ini tidak dapat dihapus karena memiliki {currentCategory.productCount} produk terkait.</strong>
            )}
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
            disabled={loading || (currentCategory?.productCount > 0)}
          >
            {loading ? <CircularProgress size={24} /> : 'Hapus'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default CategoryList;
