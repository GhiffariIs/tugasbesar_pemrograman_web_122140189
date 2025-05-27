import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { 
  AppBar, 
  Toolbar, 
  Typography, 
  Button, 
  Box,
  useScrollTrigger,
  Slide,
  Avatar
} from '@mui/material';
import aturmationLogo from '../../assets/aturmation.svg';

function HideOnScroll(props) {
  const { children } = props;
  const trigger = useScrollTrigger();

  return (
    <Slide appear={false} direction="down" in={!trigger}>
      {children}
    </Slide>
  );
}

const Navbar = () => {

  return (
    <HideOnScroll>
      <AppBar position="fixed" color="default" elevation={1}>
        <Toolbar>
          <Box 
            component={RouterLink} 
            to="/"
            sx={{ 
              display: 'flex', 
              alignItems: 'center', 
              textDecoration: 'none',
              flexGrow: 1
            }}
          >
            <Avatar 
              src={aturmationLogo} 
              alt="AturMation Logo" 
              sx={{ 
                width: 40, 
                height: 40, 
                mr: 1,
                bgcolor: 'transparent',
                '& img': {
                  objectFit: 'contain',
                  width: '100%',
                  height: '100%',
                }
              }} 
            />
            <Typography 
              variant="h6"
              sx={{ 
                fontWeight: 700,
                background: 'linear-gradient(45deg, #1976d2 30%, #21CBF3 90%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                display: { xs: 'none', sm: 'block' }
              }}
            >
              AturMation
            </Typography>
          </Box>
          
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Button 
              color="inherit" 
              component={RouterLink} 
              to="/"
              sx={{ 
                display: { xs: 'none', sm: 'inline-flex' },
                '&:hover': {
                  backgroundColor: 'rgba(25, 118, 210, 0.04)'
                }
              }}
            >
              Home
            </Button>
            <Button 
              color="inherit" 
              component={RouterLink} 
              to="/about"
              sx={{ 
                display: { xs: 'none', sm: 'inline-flex' },
                '&:hover': {
                  backgroundColor: 'rgba(25, 118, 210, 0.04)'
                }
              }}
            >
              About
            </Button>
            <Button 
              color="primary" 
              variant="outlined" 
              component={RouterLink} 
              to="/login"
              sx={{ 
                ml: 1,
                '&:hover': {
                  backgroundColor: 'rgba(25, 118, 210, 0.04)'
                }
              }}
            >
              Masuk
            </Button>
            <Button 
              color="primary" 
              variant="contained" 
              component={RouterLink} 
              to="/register"
              sx={{ 
                ml: 1,
                display: { xs: 'none', sm: 'inline-flex' },
                '&:hover': {
                  backgroundColor: '#1565c0'
                }
              }}
            >
              Daftar
            </Button>
          </Box>
        </Toolbar>
      </AppBar>
    </HideOnScroll>
  );
};

export default Navbar;
