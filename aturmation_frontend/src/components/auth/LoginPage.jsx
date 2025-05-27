import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { 
  Box, 
  Button, 
  Container, 
  TextField, 
  Typography, 
  Paper, 
  InputAdornment, 
  IconButton, 
  Link as MuiLink,
  Divider,
  CircularProgress,
  Alert
} from '@mui/material';
import { 
  LockOutlined as LockOutlinedIcon,
  PersonOutline as PersonOutlineIcon,
  Visibility,
  VisibilityOff,
  ArrowBack as ArrowBackIcon
} from '@mui/icons-material';
import { useAuth } from '../../contexts/AuthContext';
import { authService } from '../../services/services';
import { styled } from '@mui/material/styles';

const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(4),
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  maxWidth: 450,
  margin: '0 auto',
  boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)',
  borderRadius: 16,
  border: '1px solid rgba(0, 0, 0, 0.05)',
}));

const StyledAvatar = styled('div')(({ theme }) => ({
  margin: theme.spacing(1),
  backgroundColor: theme.palette.primary.main,
  padding: theme.spacing(2),
  borderRadius: '50%',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  '& svg': {
    color: theme.palette.common.white,
    fontSize: 32,
  },
}));

const StyledForm = styled('form')(({ theme }) => ({
  width: '100%',
  marginTop: theme.spacing(3),
}));

const StyledSubmitButton = styled(Button)(({ theme }) => ({
  margin: theme.spacing(3, 0, 2),
  padding: theme.spacing(1.5),
  borderRadius: 12,
  textTransform: 'none',
  fontWeight: 600,
  fontSize: '1rem',
}));

const StyledFooter = styled('div')(({ theme }) => ({
  marginTop: theme.spacing(2),
  textAlign: 'center',
  width: '100%',
}));

const LoginPage = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleTogglePassword = () => {
    setShowPassword(!showPassword);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const { username, password } = formData;
      
      if (!username || !password) {
        setError('Username dan password wajib diisi');
        setLoading(false);
        return;
      }

      const response = await authService.login(username, password);
      
      if (response.token && response.user) {
        login(response.token, response.user);
        navigate('/app/dashboard');
      } else {
        setError('Terjadi kesalahan pada respons server');
      }
    } catch (err) {
      setError(
        err.response?.data?.message || 
        'Gagal login. Periksa username dan password Anda.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container component="main" maxWidth="sm">
      <Box
        sx={{
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          py: 8,
        }}
      >
        <Box sx={{ textAlign: 'center', mb: 4 }}>
          <Typography 
            variant="h4" 
            component="h1" 
            sx={{ 
              fontWeight: 700,
              background: 'linear-gradient(45deg, #1976d2 30%, #21CBF3 90%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              mb: 1,
            }}
          >
            AturMation
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            Masuk ke akun Anda
          </Typography>
        </Box>

        <StyledPaper elevation={3}>
          <StyledAvatar>
            <LockOutlinedIcon />
          </StyledAvatar>
          
          <Typography component="h1" variant="h5" sx={{ mt: 2, fontWeight: 600 }}>
            Selamat Datang Kembali
          </Typography>
          
          <Typography variant="body2" color="text.secondary" align="center" sx={{ mt: 1, mb: 3 }}>
            Masukkan detail akun Anda untuk melanjutkan
          </Typography>

          {error && (
            <Alert severity="error" sx={{ width: '100%', mb: 2 }}>
              {error}
            </Alert>
          )}

          <StyledForm onSubmit={handleSubmit}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="username"
              label="Username"
              name="username"
              autoComplete="username"
              autoFocus
              value={formData.username}
              onChange={handleChange}
              variant="outlined"
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <PersonOutlineIcon color="action" />
                  </InputAdornment>
                ),
              }}
              sx={{ mb: 2 }}
            />
            
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type={showPassword ? 'text' : 'password'}
              id="password"
              autoComplete="current-password"
              value={formData.password}
              onChange={handleChange}
              variant="outlined"
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <LockOutlinedIcon color="action" />
                  </InputAdornment>
                ),
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      aria-label="toggle password visibility"
                      onClick={handleTogglePassword}
                      edge="end"
                      size="large"
                    >
                      {showPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />

            <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 1 }}>
              <MuiLink 
                component={Link} 
                to="/forgot-password" 
                variant="body2"
                sx={{ textDecoration: 'none' }}
              >
                Lupa password?
              </MuiLink>
            </Box>

            <StyledSubmitButton
              type="submit"
              fullWidth
              variant="contained"
              disabled={loading}
              size="large"
            >
              {loading ? <CircularProgress size={24} /> : 'Masuk'}
            </StyledSubmitButton>

            <StyledFooter>
              <Typography variant="body2" color="text.secondary">
                Belum punya akun?{' '}
                <MuiLink 
                  component={Link} 
                  to="/register" 
                  sx={{ textDecoration: 'none', fontWeight: 500 }}
                >
                  Daftar sekarang
                </MuiLink>
              </Typography>
            </StyledFooter>
          </StyledForm>
        </StyledPaper>

        <Box sx={{ mt: 4, textAlign: 'center' }}>
          <Button
            component={Link}
            to="/"
            startIcon={<ArrowBackIcon />}
            sx={{ textTransform: 'none' }}
          >
            Kembali ke Beranda
          </Button>
        </Box>
      </Box>
    </Container>
  );
};

export default LoginPage;
