import { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  CardHeader,
  Avatar,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Chip,
  ButtonGroup,
  Button,
  IconButton,
  Tooltip
} from '@mui/material';
import {
  Inventory as InventoryIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  ArrowForward as ArrowForwardIcon,
  Archive as ArchiveIcon,
  ShoppingCart as ShoppingCartIcon,
  Refresh as RefreshIcon,
  Warning as WarningIcon
} from '@mui/icons-material';
import { Link } from 'react-router-dom';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip as ChartTooltip,
  Legend,
  Filler
} from 'chart.js';
import { productService, transactionService, reportService } from '../services/services';
import { formatCurrency } from '../utils/formatters';
import { useNotifications } from '../contexts/NotificationContext';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  ChartTooltip,
  Legend,
  Filler
);

const Dashboard = () => {
  const [summary, setSummary] = useState({
    totalProducts: 0,
    totalCategories: 0,
    lowStockProducts: 0,
    todayTransactions: 0
  });
  const [recentProducts, setRecentProducts] = useState([]);
  const [recentTransactions, setRecentTransactions] = useState([]);
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: []
  });
  const [chartPeriod, setChartPeriod] = useState('week');
  const [isLoading, setIsLoading] = useState(true);
  const { lowStockItems } = useNotifications();

  useEffect(() => {
    fetchDashboardData();
  }, []);

  useEffect(() => {
    fetchChartData(chartPeriod);
  }, [chartPeriod]);

  const fetchDashboardData = async () => {
    setIsLoading(true);
    
    try {
      // In a real application, these would be actual API calls
      // For demo purposes, using mock data
      
      // Summary statistics
      setSummary({
        totalProducts: 156,
        totalCategories: 12,
        lowStockProducts: lowStockItems.length,
        todayTransactions: 24
      });
      
      // Recent products
      setRecentProducts([
        { id: 1, name: 'Laptop Asus ROG', sku: 'PRD-1234', price: 15000000, stock: 10, category: 'Laptop' },
        { id: 2, name: 'Mouse Wireless Logitech', sku: 'PRD-2345', price: 350000, stock: 25, category: 'Aksesoris' },
        { id: 3, name: 'Monitor LG 24inch', sku: 'PRD-3456', price: 2500000, stock: 8, category: 'Monitor' },
        { id: 4, name: 'Keyboard Mechanical', sku: 'PRD-4567', price: 1200000, stock: 15, category: 'Aksesoris' },
        { id: 5, name: 'Headphone Sony', sku: 'PRD-5678', price: 1800000, stock: 5, category: 'Audio' },
      ]);
      
      // Recent transactions
      setRecentTransactions([
        { id: 1, type: 'in', productName: 'Laptop Asus ROG', quantity: 5, date: '2025-05-14T09:30:00', note: 'Restock from supplier' },
        { id: 2, type: 'out', productName: 'Mouse Wireless Logitech', quantity: 3, date: '2025-05-14T10:45:00', note: 'Customer order #A001' },
        { id: 3, type: 'in', productName: 'Keyboard Mechanical', quantity: 10, date: '2025-05-13T14:20:00', note: 'New inventory' },
        { id: 4, type: 'out', productName: 'Monitor LG 24inch', quantity: 2, date: '2025-05-13T16:05:00', note: 'Customer order #A002' },
        { id: 5, type: 'out', productName: 'Headphone Sony', quantity: 1, date: '2025-05-12T11:30:00', note: 'Staff use' },
      ]);
      
      // Chart data
      fetchChartData(chartPeriod);
    } catch (error) {
      console.error("Error fetching dashboard data:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchChartData = (period) => {
    // Mock data for chart - would be fetched from API in real app
    let labels = [];
    let stockInData = [];
    let stockOutData = [];
    
    if (period === 'week') {
      labels = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'];
      stockInData = [12, 19, 8, 15, 20, 14, 11];
      stockOutData = [8, 12, 10, 9, 14, 18, 10];
    } else if (period === 'month') {
      labels = ['Minggu 1', 'Minggu 2', 'Minggu 3', 'Minggu 4'];
      stockInData = [45, 52, 38, 60];
      stockOutData = [35, 42, 29, 48];
    } else { // year
      labels = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'];
      stockInData = [100, 120, 115, 130, 140, 125, 135, 145, 150, 160, 170, 180];
      stockOutData = [80, 90, 85, 100, 110, 95, 105, 115, 125, 130, 140, 150];
    }
    
    setChartData({
      labels,
      datasets: [
        {
          label: 'Barang Masuk',
          data: stockInData,
          borderColor: '#4CAF50',
          backgroundColor: 'rgba(76, 175, 80, 0.1)',
          tension: 0.3,
          fill: true
        },
        {
          label: 'Barang Keluar',
          data: stockOutData,
          borderColor: '#F44336',
          backgroundColor: 'rgba(244, 67, 54, 0.1)',
          tension: 0.3,
          fill: true
        }
      ]
    });
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Transaksi Barang',
        font: {
          size: 16
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true
      }
    }
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Dashboard
      </Typography>
      
      <Grid container spacing={3} sx={{ mb: 6, display: 'grid', gap: 2, gridTemplateColumns: 'repeat(2, 1fr)'}}>
        {/* Summary Cards */}
        <Grid item xs={12} sm={6} md={3}>
          <Paper
            elevation={2}
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              borderLeft: '4px solid #1976D2'
            }}
          >
            <Typography variant="subtitle2" color="text.secondary">
              Total Produk
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Typography variant="h4" component="div">
                {summary.totalProducts}
              </Typography>
              <Avatar sx={{ bgcolor: 'primary.light' }}>
                <InventoryIcon />
              </Avatar>
            </Box>
            <Link to="/products" style={{ textDecoration: 'none', marginTop: '8px', display: 'flex', alignItems: 'center' }}>
              <Typography variant="body2" color="primary">
                Lihat Detail
              </Typography>
              <ArrowForwardIcon fontSize="small" sx={{ ml: 0.5 }} />
            </Link>
          </Paper>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Paper
            elevation={2}
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              borderLeft: '4px solid #FFC107'
            }}
          >
            <Typography variant="subtitle2" color="text.secondary">
              Total Kategori
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Typography variant="h4" component="div">
                {summary.totalCategories}
              </Typography>
              <Avatar sx={{ bgcolor: 'warning.light' }}>
                <ArchiveIcon />
              </Avatar>
            </Box>
            <Link to="/categories" style={{ textDecoration: 'none', marginTop: '8px', display: 'flex', alignItems: 'center' }}>
              <Typography variant="body2" color="primary">
                Lihat Detail
              </Typography>
              <ArrowForwardIcon fontSize="small" sx={{ ml: 0.5 }} />
            </Link>
          </Paper>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Paper
            elevation={2}
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              borderLeft: '4px solid #F44336'
            }}
          >
            <Typography variant="subtitle2" color="text.secondary">
              Stok Rendah
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Typography variant="h4" component="div">
                {summary.lowStockProducts}
              </Typography>
              <Avatar sx={{ bgcolor: 'error.light' }}>
                <WarningIcon />
              </Avatar>
            </Box>
            <Link to="/products?filter=low-stock" style={{ textDecoration: 'none', marginTop: '8px', display: 'flex', alignItems: 'center' }}>
              <Typography variant="body2" color="primary">
                Lihat Detail
              </Typography>
              <ArrowForwardIcon fontSize="small" sx={{ ml: 0.5 }} />
            </Link>
          </Paper>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Paper
            elevation={2}
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              borderLeft: '4px solid #4CAF50'
            }}
          >
            <Typography variant="subtitle2" color="text.secondary">
              Transaksi Hari Ini
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Typography variant="h4" component="div">
                {summary.todayTransactions}
              </Typography>
              <Avatar sx={{ bgcolor: 'success.light' }}>
                <ShoppingCartIcon />
              </Avatar>
            </Box>
            <Link to="/transactions" style={{ textDecoration: 'none', marginTop: '8px', display: 'flex', alignItems: 'center' }}>
              <Typography variant="body2" color="primary">
                Lihat Detail
              </Typography>
              <ArrowForwardIcon fontSize="small" sx={{ ml: 0.5 }} />
            </Link>
          </Paper>
        </Grid>
        
        {/* Chart */}
        <Grid item xs={12} md={8}>
          <Card elevation={2}>
            <CardHeader 
              title="Grafik Transaksi"
              action={
                <Box>
                  <ButtonGroup size="small">
                    <Button 
                      variant={chartPeriod === 'week' ? 'contained' : 'outlined'} 
                      onClick={() => setChartPeriod('week')}
                    >
                      Minggu
                    </Button>
                    <Button 
                      variant={chartPeriod === 'month' ? 'contained' : 'outlined'} 
                      onClick={() => setChartPeriod('month')}
                    >
                      Bulan
                    </Button>
                    <Button 
                      variant={chartPeriod === 'year' ? 'contained' : 'outlined'} 
                      onClick={() => setChartPeriod('year')}
                    >
                      Tahun
                    </Button>
                  </ButtonGroup>
                  <Tooltip title="Refresh">
                    <IconButton 
                      size="small" 
                      onClick={() => fetchChartData(chartPeriod)}
                      sx={{ ml: 1 }}
                    >
                      <RefreshIcon />
                    </IconButton>
                  </Tooltip>
                </Box>
              }
            />
            <CardContent>
              <div style={{ height: '300px' }}>
                <Line options={chartOptions} data={chartData} />
              </div>
            </CardContent>
          </Card>
        </Grid>
        
        {/* Low Stock Items */}
        <Grid item xs={12} md={4}>
          <Card elevation={2} sx={{ height: '100%' }}>
            <CardHeader 
              title="Produk Stok Rendah" 
              titleTypographyProps={{ variant: 'h6' }}
            />
            <CardContent sx={{ pt: 0, pb: 1 }}>
              {lowStockItems.length > 0 ? (
                <List disablePadding>
                  {lowStockItems.map((item) => (
                    <Box key={item.id}>
                      <ListItem 
                        disablePadding 
                        sx={{ py: 1 }}
                        secondaryAction={
                          <Chip
                            label={`${item.currentStock}/${item.minStock}`}
                            color="error"
                            size="small"
                          />
                        }
                      >
                        <ListItemText 
                          primary={item.name}
                          primaryTypographyProps={{ variant: 'body2' }}
                        />
                      </ListItem>
                      <Divider component="li" />
                    </Box>
                  ))}
                </List>
              ) : (
                <Typography variant="body2" color="text.secondary" align="center">
                  Tidak ada produk dengan stok rendah
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>
        
        {/* Recent Products */}
        <Grid item xs={12} md={6}>
          <Card elevation={2}>
            <CardHeader 
              title="Produk Terbaru" 
              titleTypographyProps={{ variant: 'h6' }}
              action={
                <Button 
                  size="small" 
                  endIcon={<ArrowForwardIcon />}
                  component={Link}
                  to="/products"
                >
                  Lihat Semua
                </Button>
              }
            />
            <Divider />
            <CardContent sx={{ p: 0 }}>
              <List disablePadding>
                {recentProducts.map((product) => (
                  <Box key={product.id}>
                    <ListItem
                      disablePadding
                      sx={{ px: 2, py: 1 }}
                      secondaryAction={
                        <Typography variant="body2" color="text.secondary">
                          Stok: {product.stock}
                        </Typography>
                      }
                    >
                      <ListItemAvatar>
                        <Avatar sx={{ bgcolor: 'primary.light' }}>
                          <InventoryIcon />
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText
                        primary={product.name}
                        secondary={
                          <>
                            <Typography component="span" variant="body2" color="text.primary">
                              {formatCurrency(product.price)}
                            </Typography>
                            <Typography component="span" variant="body2" color="text.secondary">
                              {` • ${product.category}`}
                            </Typography>
                          </>
                        }
                      />
                    </ListItem>
                    <Divider component="li" />
                  </Box>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
        
        {/* Recent Transactions */}
        <Grid item xs={12} md={6}>
          <Card elevation={2}>
            <CardHeader 
              title="Transaksi Terbaru" 
              titleTypographyProps={{ variant: 'h6' }}
              action={
                <Button 
                  size="small" 
                  endIcon={<ArrowForwardIcon />}
                  component={Link}
                  to="/transactions"
                >
                  Lihat Semua
                </Button>
              }
            />
            <Divider />
            <CardContent sx={{ p: 0 }}>
              <List disablePadding>
                {recentTransactions.map((transaction) => (
                  <Box key={transaction.id}>
                    <ListItem
                      disablePadding
                      sx={{ px: 2, py: 1 }}
                    >
                      <ListItemAvatar>
                        <Avatar
                          sx={{
                            bgcolor: transaction.type === 'in' ? 'success.light' : 'error.light'
                          }}
                        >
                          {transaction.type === 'in' ? <TrendingUpIcon /> : <TrendingDownIcon />}
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText
                        primary={transaction.productName}
                        secondary={
                          <Typography variant="caption" color="text.secondary">
                            {transaction.note}
                          </Typography>
                        }
                      />
                      <Box textAlign="right">
                        <Typography variant="body2" color={transaction.type === 'in' ? 'success.main' : 'error.main'}>
                          {transaction.type === 'in' ? '+' : '-'}{transaction.quantity}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {new Date(transaction.date).toLocaleDateString('id-ID')}
                        </Typography>
                      </Box>
                    </ListItem>
                    <Divider component="li" />
                  </Box>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
