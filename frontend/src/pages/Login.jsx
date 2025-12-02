import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Box,
  Paper,
  TextField,
  Button,
  Typography,
  Alert,
  CircularProgress,
} from '@mui/material'
import { Login as LoginIcon } from '@mui/icons-material'
import { useAuth } from '../contexts/AuthContext'
import { useLanguage } from '../contexts/LanguageContext'
import { useTranslation } from '../translations/translations'

function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const { login } = useAuth()
  const navigate = useNavigate()
  const { language } = useLanguage()
  const t = useTranslation(language)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    const result = await login(username, password)

    if (result.success) {
      navigate('/dashboard')
    } else {
      setError(result.error || t('login.error'))
    }

    setLoading(false)
  }

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #32373c 0%, #00a6bc 50%, #75cede 100%)',
        padding: 3,
      }}
    >
      <Paper
        elevation={10}
        sx={{
          padding: 4,
          maxWidth: 400,
          width: '100%',
          borderRadius: 3,
        }}
      >
        <Box sx={{ textAlign: 'center', mb: 3 }}>
          <Box
            component="img"
            src="/assets/logo_fcp_branco-768x352.png"
            alt="FCP Logo"
            sx={{
              width: '80%',
              maxWidth: 200,
              height: 'auto',
              mb: 2,
              filter: 'brightness(0) saturate(100%) invert(48%) sepia(79%) saturate(2476%) hue-rotate(164deg) brightness(92%) contrast(101%)',
            }}
          />
          <Typography variant="h5" sx={{ fontWeight: 'bold', color: '#32373c' }}>
            {t('login.title')}
          </Typography>
          <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
            {t('login.welcome')}
          </Typography>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            label={t('login.username')}
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            margin="normal"
            required
            autoFocus
            sx={{
              '& .MuiOutlinedInput-root': {
                '&:hover fieldset': {
                  borderColor: '#00a6bc',
                },
                '&.Mui-focused fieldset': {
                  borderColor: '#00a6bc',
                },
              },
              '& .MuiInputLabel-root.Mui-focused': {
                color: '#00a6bc',
              },
            }}
          />
          <TextField
            fullWidth
            type="password"
            label={t('login.password')}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            margin="normal"
            required
            sx={{
              '& .MuiOutlinedInput-root': {
                '&:hover fieldset': {
                  borderColor: '#00a6bc',
                },
                '&.Mui-focused fieldset': {
                  borderColor: '#00a6bc',
                },
              },
              '& .MuiInputLabel-root.Mui-focused': {
                color: '#00a6bc',
              },
            }}
          />
          <Button
            fullWidth
            type="submit"
            variant="contained"
            size="large"
            startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <LoginIcon />}
            disabled={loading}
            sx={{
              mt: 3,
              mb: 2,
              py: 1.5,
              background: 'linear-gradient(135deg, #00a6bc 0%, #75cede 100%)',
              '&:hover': {
                background: 'linear-gradient(135deg, #008394 0%, #00a6bc 100%)',
              },
            }}
          >
            {t('login.button')}
          </Button>
        </form>
      </Paper>
    </Box>
  )
}

export default Login
