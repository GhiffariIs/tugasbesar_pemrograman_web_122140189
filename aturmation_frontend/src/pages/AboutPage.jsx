import React from 'react';
import { Box, Container, Typography, Grid, Paper, useTheme, useMediaQuery } from '@mui/material';
import Navbar from '../components/layout/Navbar';

const AboutPage = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Navbar />
      <Box component="main" sx={{ flexGrow: 1, py: 8, margin: 4 }}>
        <Container maxWidth="lg">
          <Typography 
            variant={isMobile ? 'h4' : 'h3'} 
            component="h1" 
            gutterBottom 
            align="center"
            sx={{
              fontWeight: 700,
              mb: 6,
              background: 'linear-gradient(45deg, #1976d2 30%, #21CBF3 90%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}
          >
            Tentang AturMation
          </Typography>
          
          <Grid container spacing={4} sx={{ mb: 6, display: 'grid', gap: 1, gridTemplateColumns: 'repeat(2, 1fr)'}}> 
            <Grid item xs={12} md={6}>
              <Paper 
                elevation={3} 
                sx={{ 
                  p: 4, 
                  height: '100%', 
                  minHeight: 300,
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'center',
                  textAlign: 'center',
                  borderRadius: 3,
                  transition: 'transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out',
                  '&:hover': {
                    transform: 'translateY(-5px)',
                    boxShadow: 6
                  }
                }}
              >
                <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                  <Typography variant="h5" component="h2" gutterBottom sx={{ fontWeight: 700, mb: 3, color: 'primary.main' }}>
                    Visi Kami
                  </Typography>
                  <Box sx={{ maxWidth: 500, mx: 'auto' }}>
                    <Typography variant="body1" paragraph sx={{ mb: 3, lineHeight: 1.8 }}>
                      Menjadi solusi manajemen inventori terdepan yang membantu bisnis mengoptimalkan operasional mereka dengan teknologi terkini.
                    </Typography>
                    <Typography variant="body1" sx={{ fontStyle: 'italic', color: 'text.secondary' }}>
                      "Kami percaya bahwa manajemen inventori yang baik adalah kunci kesuksesan bisnis di era digital ini."
                    </Typography>
                  </Box>
                </Box>
              </Paper>
            </Grid>
            
            <Grid item xs={12} md={6} >
              <Paper 
                elevation={3} 
                sx={{ 
                  p: 4, 
                  height: '100%',
                  minHeight: 300,
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'center',
                  textAlign: 'center',
                  borderRadius: 3,
                  transition: 'transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out',
                  '&:hover': {
                    transform: 'translateY(-5px)',
                    boxShadow: 6
                  }
                }}
              >
                <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                  <Typography variant="h5" component="h2" gutterBottom sx={{ fontWeight: 700, mb: 3, color: 'primary.main' }}>
                    Misi Kami
                  </Typography>
                  <Box sx={{ maxWidth: 500, mx: 'auto' }}>
                    {[
                      'Menyediakan platform manajemen inventori yang mudah digunakan dan andal',
                      'Meningkatkan efisiensi operasional bisnis pelanggan',
                      'Memberikan dukungan terbaik untuk kesuksesan bisnis Anda'
                    ].map((item, index) => (
                      <Box 
                        key={index} 
                        sx={{ 
                          display: 'flex', 
                          alignItems: 'flex-start',
                          mb: 2,
                          textAlign: 'left',
                          '&:last-child': { mb: 0 }
                        }}
                      >
                        <Box sx={{ 
                          width: 24, 
                          height: 24, 
                          borderRadius: '50%', 
                          bgcolor: 'primary.main', 
                          color: 'white',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          mr: 2,
                          mt: '2px',
                          flexShrink: 0
                        }}>
                          {index + 1}
                        </Box>
                        <Typography variant="body1" sx={{ lineHeight: 1.6 }}>{item}</Typography>
                      </Box>
                    ))}
                  </Box>
                </Box>
              </Paper>
            </Grid>
            
            <Grid item xs={12} sx={{ gridColumn: 'span 2'}}>
              <Paper elevation={3} sx={{ p: 4, mt: 2 }}>
                <Typography variant="h5" component="h2" gutterBottom align="center" sx={{ fontWeight: 600, mb: 4 }}>
                  Kenapa Memilih AturMation?
                </Typography>
                
                <Grid container spacing={4} sx={{ display: 'grid', gap: 1, gridTemplateColumns: 'repeat(2, 1fr)' }}>
                  {[
                    {
                      title: 'Mudah Digunakan',
                      description: 'Antarmuka yang intuitif dan mudah dipahami oleh semua pengguna.'
                    },
                    {
                      title: 'Fitur Lengkap',
                      description: 'Dilengkapi dengan berbagai fitur untuk mengelola inventori bisnis Anda.'
                    },
                    {
                      title: 'Keamanan Terjamin',
                      description: 'Data bisnis Anda aman dengan sistem keamanan terenkripsi.'
                    },
                    {
                      title: 'Dukungan 24/7',
                      description: 'Tim dukungan kami siap membantu kapan saja Anda membutuhkan.'
                    }
                  ].map((feature, index) => (
                    <Grid item xs={12} sm={6} key={index} sx={{ placeSelf: 'center'}}>
                      <Box sx={{ textAlign: 'center', width: 1}}>
                        <Box 
                          sx={{
                            width: 80,
                            height: 80,
                            borderRadius: '50%',
                            bgcolor: 'primary.light',
                            display: 'inline-flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            mb: 2,
                            color: 'primary.contrastText',
                            fontSize: '1.5rem',
                            fontWeight: 'bold'
                          }}
                        >
                          {index + 1}
                        </Box>
                        <Typography variant="h6" component="h3" gutterBottom>
                          {feature.title}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {feature.description}
                        </Typography>
                      </Box>
                    </Grid>
                  ))}
                </Grid>
              </Paper>
            </Grid>
          </Grid>
        </Container>
      </Box>
    </Box>
  );
};

export default AboutPage;
