import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Box, 
  Button, 
  Container, 
  Typography, 
  Grid, 
  Card, 
  CardContent, 
  useTheme,
  useMediaQuery,
  Toolbar,
  Avatar
} from '@mui/material';
import { styled } from '@mui/material/styles';
import Navbar from '../layout/Navbar';
import aturmationLogo from '../../assets/aturmation.svg';

const HeroSection = styled(Box)(({ theme }) => ({
  minHeight: '100vh',
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
  background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
  padding: theme.spacing(8, 0),
  textAlign: 'center',
}));

const FeatureCard = styled(Card)(({ theme }) => ({
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
  transition: 'all 0.3s ease-in-out',
  borderRadius: '16px',
  overflow: 'hidden',
  '&:hover': {
    transform: 'translateY(-8px)',
    boxShadow: '0 10px 30px rgba(0, 0, 0, 0.1)',
    '& .feature-icon': {
      transform: 'scale(1.1)',
      backgroundColor: theme.palette.primary.light,
    }
  },
}));

const FeatureIcon = styled(Box)(({ theme }) => ({
  width: '80px',
  height: '80px',
  margin: '0 auto 24px',
  borderRadius: '50%',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  backgroundColor: theme.palette.primary.main,
  color: theme.palette.common.white,
  fontSize: '2.5rem',
  transition: 'all 0.3s ease-in-out',
}));

const LandingPage = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  const features = [
    {
      title: 'Manajemen Produk',
      description: 'Kelola stok produk dengan mudah dan efisien',
      icon: '📦',
      md: 6,
      lg: 6
    },
    {
      title: 'Kategori Terstruktur',
      description: 'Kelompokkan produk dengan kategori yang terorganisir',
      icon: '🏷️',
      md: 6,
      lg: 6
    },
    {
      title: 'Laporan Transaksi',
      description: 'Pantau semua transaksi dengan laporan yang lengkap',
      icon: '📊',
      md: 6,
      lg: 6
    },
  ];

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Navbar />
      <Toolbar /> {/* This pushes content below the fixed AppBar */}
      {/* Hero Section */}
      <HeroSection>
        <Container maxWidth="md">
          <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mb: 4 }}>
            <Avatar 
              src={aturmationLogo} 
              alt="AturMation Logo" 
              sx={{ 
                width: 120, 
                height: 120, 
                mb: 3,
                bgcolor: 'transparent',
                '& img': {
                  objectFit: 'contain',
                  width: '100%',
                  height: '100%',
                }
              }} 
            />
            <Typography 
              variant={isMobile ? 'h3' : 'h2'} 
              component="h1" 
              sx={{
                fontWeight: 700,
                background: 'linear-gradient(45deg, #1976d2 30%, #21CBF3 90%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                textAlign: 'center',
              }}
            >
              AturMation
            </Typography>
          </Box>
          <Typography 
            variant={isMobile ? 'h6' : 'h5'} 
            color="text.secondary" 
            paragraph
            sx={{ mb: 4 }}
          >
            Solusi Manajemen Inventori Modern untuk Bisnis Anda
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap', mt: 4 }}>
            <Button 
              component={Link} 
              to="/login" 
              variant="contained" 
              size="large"
              sx={{ px: 4, py: 1.5, display: { xs: 'inline-flex', sm: 'none' } }}
            >
              Masuk
            </Button>
            <Button 
              component={Link} 
              to="/register" 
              variant="outlined" 
              size="large"
              sx={{ px: 4, py: 1.5, display: { xs: 'inline-flex', sm: 'none' } }}
            >
              Daftar
            </Button>
          </Box>
        </Container>
      </HeroSection>

      {/* Features Section */}
      <Box sx={{ py: { xs: 6, md: 10 }, bgcolor: 'background.paper' }}>
        <Container maxWidth="lg">
          <Box sx={{ textAlign: 'center', mb: { xs: 4, md: 8 }, maxWidth: 800, mx: 'auto', px: 2 }}>
            <Typography 
              variant="h3" 
              component="h2"
              sx={{ 
                fontWeight: 700, 
                mb: 2,
                background: 'linear-gradient(45deg, #1976d2 30%, #21CBF3 90%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
              }}
            >
              Fitur Unggulan
            </Typography>
            <Typography 
              variant="h6" 
              color="text.secondary"
              sx={{ maxWidth: 600, mx: 'auto', mb: 1 }}
            >
              Solusi lengkap untuk manajemen inventori bisnis Anda
            </Typography>
          </Box>
          
          <Grid 
            container 
            spacing={{ xs: 3, md: 4 }}
            sx={{
              '& .MuiGrid-item': {
                display: 'flex',
                flexDirection: 'column',
                '&:last-child': {
                  ml: { lg: 'auto' }
                }
              },
              position: 'relative',
              alignItems: 'flex-start'
            }}
          >
            {features.map((feature, index) => (
              <Grid 
                item 
                key={index} 
                xs={12} 
                sm={6} 
                md={feature.md || 6}
                lg={feature.lg || 4}
                sx={feature.sx}
              >
                <FeatureCard elevation={0}>
                  <CardContent sx={{ 
                    flexGrow: 2, 
                    textAlign: 'center',
                    p: { xs: 3, md: 3 },
                    '&:last-child': { pb: { xs: 3, md: 3 } }
                  }}>
                    <FeatureIcon className="feature-icon">
                      {feature.icon}
                    </FeatureIcon>
                    <Typography 
                      variant="h5" 
                      component="h3" 
                      gutterBottom
                      sx={{ 
                        fontWeight: 600,
                        mb: 2,
                        color: 'text.primary'
                      }}
                    >
                      {feature.title}
                    </Typography>
                    <Typography 
                      variant="body1" 
                      color="text.secondary"
                      sx={{ 
                        lineHeight: 1.7,
                        maxWidth: 300,
                        mx: 'auto'
                      }}
                    >
                      {feature.description}
                    </Typography>
                  </CardContent>
                </FeatureCard>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>

      {/* Footer */}
      <Box component="footer" sx={{ py: 6, bgcolor: 'background.default' }}>
        <Container maxWidth="md">
          <Typography variant="body2" color="text.secondary" align="center">
            © {new Date().getFullYear()} AturMation. All rights reserved.
          </Typography>
        </Container>
      </Box>
    </Box>
  );
};

export default LandingPage;
