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
  Alert,
  Grid
} from '@mui/material';
import { 
  PersonAdd as PersonAddIcon,
  PersonOutline as PersonOutlineIcon,
  EmailOutlined as EmailOutlinedIcon,
  LockOutlined as LockOutlinedIcon,
  Visibility,
  VisibilityOff,
  ArrowBack as ArrowBackIcon
} from '@mui/icons-material';
import { useAuth } from '../../contexts/AuthContext';
import { authService } from '../../services/services';
import { isValidEmail } from '../../utils/formatters';
import { styled } from '@mui/material/styles';

const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(4, 3),
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  width: '100%',
  maxWidth: 500,
  boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)',
  borderRadius: 12,
  border: '1px solid rgba(0, 0, 0, 0.05)',
  [theme.breakpoints.down('sm')]: {
    padding: theme.spacing(3, 2),
  },
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
  marginTop: theme.spacing(1),
  '& .MuiTextField-root': {
    marginBottom: theme.spacing(2),
    '&:last-child': {
      marginBottom: 0
    }
  },
}));

const StyledSubmitButton = styled(Button)(({ theme }) => ({
  margin: theme.spacing(2, 0, 1),
  padding: theme.spacing(1.25),
  borderRadius: 8,
  textTransform: 'none',
  fontWeight: 600,
  fontSize: '1rem',
  width: '100%',
  height: 48,
}));

const StyledFooter = styled('div')(({ theme }) => ({
  marginTop: theme.spacing(2),
  textAlign: 'center',
  width: '100%',
}));

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    name: '',
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [errors, setErrors] = useState({});
  const [serverError, setServerError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    
    // Clear validation error when user types
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };


  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.name.trim()) {
      newErrors.name = 'Nama wajib diisi';
    }
    
    if (!formData.username.trim()) {
      newErrors.username = 'Username wajib diisi';
    } else if (formData.username.length < 4) {
      newErrors.username = 'Username minimal 4 karakter';
    }
    
    if (!formData.email.trim()) {
      newErrors.email = 'Email wajib diisi';
    } else if (!isValidEmail(formData.email)) {
      newErrors.email = 'Format email tidak valid';
    }
    
    if (!formData.password) {
      newErrors.password = 'Password wajib diisi';
    } else if (formData.password.length < 6) {
      newErrors.password = 'Password minimal 6 karakter';
    }
    
    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Password tidak sama';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setServerError('');
    
    // Validate form fields
    if (!validateForm()) {
      return;
    }
    
    setLoading(true);
    
    try {
      const { name, username, email, password } = formData;
      
      const registerData = {
        name,
        username,
        email,
        password
      };
      
      const response = await authService.register(registerData);
      
      if (response.token && response.user) {
        login(response.token, response.user);
        navigate('/dashboard');
      } else {
        setServerError('Terjadi kesalahan pada respons server');
      }
    } catch (err) {
      setServerError(
        err.response?.data?.message || 
        'Gagal mendaftar. Silakan coba dengan data yang berbeda.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      component="main"
      sx={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        py: { xs: 2, sm: 4 },
        px: { xs: 2, sm: 3 },
      }}
    >
      <Container maxWidth="sm" sx={{ width: '100%' }}>
        <StyledPaper elevation={3}>
          <Box>
          <StyledAvatar>
              <PersonAddIcon />
            </StyledAvatar>
          </Box>
          <Box sx={{ width: '100%', textAlign: 'center', mb: 4 }}>
            <Typography 
              variant="h5" 
              component="h1" 
              sx={{ 
                fontWeight: 700,
                mt: 2,
                mb: 1,
                color: 'text.primary',
              }}
            >
              Buat Akun Baru
            </Typography>
            <Typography variant="subtitle1" color="text.secondary">
              Buat akun baru
            </Typography>
          </Box>

          {serverError && (
            <Alert 
              severity="error" 
              sx={{ 
                mb: 2,
                '& .MuiAlert-message': {
                  width: '100%',
                }
              }}
            >
              {serverError}
            </Alert>
          )}
          <StyledForm onSubmit={handleSubmit}>
            <TextField
              fullWidth
              label="Nama Lengkap"
              name="name"
              value={formData.name}
              onChange={handleChange}
              error={!!errors.name}
              helperText={errors.name}
              variant="outlined"
              size="small"
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <PersonOutlineIcon color="action" />
                  </InputAdornment>
                ),
              }}
            />

            <TextField
              fullWidth
              label="Username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              error={!!errors.username}
              helperText={errors.username}
              variant="outlined"
              size="small"
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <PersonOutlineIcon color="action" />
                  </InputAdornment>
                ),
              }}
            />

            <TextField
              fullWidth
              label="Email"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              error={!!errors.email}
              helperText={errors.email}
              variant="outlined"
              size="small"
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <EmailOutlinedIcon color="action" />
                  </InputAdornment>
                ),
              }}
            />

            <TextField
              fullWidth
              label="Password"
              name="password"
              type={showPassword ? 'text' : 'password'}
              value={formData.password}
              onChange={handleChange}
              error={!!errors.password}
              helperText={errors.password}
              variant="outlined"
              size="small"
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <LockOutlinedIcon color="action" />
                  </InputAdornment>
                ),
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      size="small"
                      aria-label="toggle password visibility"
                      onClick={() => setShowPassword(!showPassword)}
                      edge="end"
                    >
                      {showPassword ? <VisibilityOff fontSize="small" /> : <Visibility fontSize="small" />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />

            <TextField
              fullWidth
              label="Konfirmasi Password"
              name="confirmPassword"
              type={showPassword ? 'text' : 'password'}
              value={formData.confirmPassword}
              onChange={handleChange}
              error={!!errors.confirmPassword}
              helperText={errors.confirmPassword}
              variant="outlined"
              size="small"
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <LockOutlinedIcon color="action" />
                  </InputAdornment>
                ),
              }}
            />

            {serverError && (
              <Alert 
                severity="error" 
                sx={{ 
                  mt: 1, 
                  mb: 1,
                  '& .MuiAlert-message': {
                    width: '100%',
                    textAlign: 'left',
                  }
                }}
              >
                {serverError}
              </Alert>
            )}

            <StyledSubmitButton
              type="submit"
              variant="contained"
              color="primary"
              disabled={loading}
              startIcon={loading ? <CircularProgress size={20} color="inherit" /> : null}
            >
              {loading ? 'Mendaftar...' : 'Daftar'}
            </StyledSubmitButton>

            <StyledFooter>
              <Typography variant="body2" color="text.secondary">
                Sudah punya akun?{' '}
                <MuiLink component={Link} to="/login" color="primary">
                  Masuk di sini
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
      </Container>
    </Box>
  );
};

export default RegisterPage;
