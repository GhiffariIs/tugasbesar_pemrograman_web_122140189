import React from 'react';
import { Box, Container, Typography, Grid, Paper, useTheme, useMediaQuery } from '@mui/material';
import Navbar from '../layout/Navbar';

const AboutPage = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Navbar />
      <Box component="main" sx={{ flexGrow: 1, py: 8 }}>
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
          
          <Grid container spacing={4}>
            <Grid item xs={12} md={6}>
              <Paper elevation={3} sx={{ p: 4, height: '100%' }}>
                <Typography variant="h5" component="h2" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
                  Visi Kami
                </Typography>
                <Typography variant="body1" paragraph>
                  Menjadi solusi manajemen inventori terdepan yang membantu bisnis mengoptimalkan operasional mereka dengan teknologi terkini.
                </Typography>
                <Typography variant="body1">
                  Kami percaya bahwa manajemen inventori yang baik adalah kunci kesuksesan bisnis di era digital ini.
                </Typography>
              </Paper>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Paper elevation={3} sx={{ p: 4, height: '100%' }}>
                <Typography variant="h5" component="h2" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
                  Misi Kami
                </Typography>
                <Typography variant="body1" paragraph>
                  - Menyediakan platform manajemen inventori yang mudah digunakan dan andal
                </Typography>
                <Typography variant="body1" paragraph>
                  - Meningkatkan efisiensi operasional bisnis pelanggan
                </Typography>
                <Typography variant="body1">
                  - Memberikan dukungan terbaik untuk kesuksesan bisnis Anda
                </Typography>
              </Paper>
            </Grid>
            
            <Grid item xs={12}>
              <Paper elevation={3} sx={{ p: 4, mt: 2 }}>
                <Typography variant="h5" component="h2" gutterBottom align="center" sx={{ fontWeight: 600, mb: 4 }}>
                  Kenapa Memilih AturMation?
                </Typography>
                
                <Grid container spacing={4}>
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
                    <Grid item xs={12} sm={6} key={index}>
                      <Box sx={{ textAlign: 'center' }}>
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
