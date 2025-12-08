import { useState } from 'react'
import {
  Box,
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Alert,
  CircularProgress,
  ToggleButtonGroup,
  ToggleButton,
} from '@mui/material'
import {
  Unsubscribe as UnsubscribeIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
} from '@mui/icons-material'
import { useLanguage } from '../contexts/LanguageContext'
import { useTranslation } from '../translations/translations'
import { leadsAPI } from '../services/api'

function Unsubscribe() {
  const [formData, setFormData] = useState({
    email: '',
    reason: '',
    comments: '',
  })
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState(false)
  const [validationErrors, setValidationErrors] = useState({})
  const { language, changeLanguage } = useLanguage()
  const t = useTranslation(language)

  const validateForm = () => {
    const errors = {}

    if (!formData.email) {
      errors.email = t('unsubscribe.requiredEmail')
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      errors.email = 'Email inválido'
    }

    if (!formData.reason) {
      errors.reason = t('unsubscribe.requiredReason')
    }

    setValidationErrors(errors)
    return Object.keys(errors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!validateForm()) {
      return
    }

    setLoading(true)
    setError(false)

    try {
      // Chama o endpoint do backend para cancelar inscrição
      await leadsAPI.unsubscribe({
        email: formData.email,
        reason: formData.reason,
        comments: formData.comments,
      })

      setSuccess(true)
      setFormData({ email: '', reason: '', comments: '' })
    } catch (err) {
      console.error('Erro ao cancelar inscrição:', err)
      setError(true)
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (field, value) => {
    setFormData({ ...formData, [field]: value })
    // Limpar erro de validação ao digitar
    if (validationErrors[field]) {
      setValidationErrors({ ...validationErrors, [field]: '' })
    }
  }

  if (success) {
    return (
      <Box
        sx={{
          minHeight: '100vh',
          background: 'linear-gradient(135deg, #00a6bc 0%, #32373c 100%)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          py: 4,
        }}
      >
        <Container maxWidth="sm">
          <Paper
            elevation={10}
            sx={{
              p: 4,
              borderRadius: 3,
              textAlign: 'center',
            }}
          >
            <CheckCircleIcon
              sx={{
                fontSize: 80,
                color: '#4caf50',
                mb: 2,
              }}
            />
            <Typography variant="h4" gutterBottom sx={{ fontWeight: 'bold', color: '#32373c' }}>
              {t('unsubscribe.successTitle')}
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
              {t('unsubscribe.successMessage')}
            </Typography>
            <Button
              variant="contained"
              onClick={() => window.location.href = 'https://federacioncolombianadepoker.com.co/'}
              sx={{
                backgroundColor: '#00a6bc',
                '&:hover': {
                  backgroundColor: '#008394',
                },
              }}
            >
              {t('unsubscribe.cancelButton')}
            </Button>
          </Paper>
        </Container>
      </Box>
    )
  }

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #00a6bc 0%, #32373c 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        py: 4,
      }}
    >
      <Container maxWidth="sm">
        <Paper
          elevation={10}
          sx={{
            p: 4,
            borderRadius: 3,
          }}
        >
          {/* Logo e Header */}
          <Box sx={{ textAlign: 'center', mb: 3 }}>
            <Box
              component="img"
              src="/assets/logo_fcp_branco-768x352.png"
              alt="Federación Colombiana de Póker"
              sx={{
                width: '60%',
                maxWidth: '250px',
                height: 'auto',
                mb: 2,
                filter: 'brightness(0) saturate(100%) invert(18%) sepia(8%) saturate(1168%) hue-rotate(169deg) brightness(94%) contrast(88%)',
              }}
            />
            <UnsubscribeIcon
              sx={{
                fontSize: 50,
                color: '#d32f2f',
                mb: 1,
              }}
            />
            <Typography variant="h4" gutterBottom sx={{ fontWeight: 'bold', color: '#32373c' }}>
              {t('unsubscribe.title')}
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              {t('unsubscribe.subtitle')}
            </Typography>

            {/* Language Selector */}
            <ToggleButtonGroup
              value={language}
              exclusive
              onChange={(e, newLang) => newLang && changeLanguage(newLang)}
              size="small"
              sx={{
                mb: 2,
                '& .MuiToggleButton-root': {
                  borderColor: '#00a6bc',
                  color: '#00a6bc',
                  px: 3,
                  '&.Mui-selected': {
                    backgroundColor: '#00a6bc',
                    color: 'white',
                    '&:hover': {
                      backgroundColor: '#008394',
                    },
                  },
                },
              }}
            >
              <ToggleButton value="pt">PT</ToggleButton>
              <ToggleButton value="es">ES</ToggleButton>
            </ToggleButtonGroup>
          </Box>

          {/* Error Alert */}
          {error && (
            <Alert
              severity="error"
              icon={<ErrorIcon />}
              sx={{ mb: 3 }}
              onClose={() => setError(false)}
            >
              <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                {t('unsubscribe.errorTitle')}
              </Typography>
              <Typography variant="caption">
                {t('unsubscribe.errorMessage')}
              </Typography>
            </Alert>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit}>
            <TextField
              fullWidth
              label={t('unsubscribe.emailLabel')}
              placeholder={t('unsubscribe.emailPlaceholder')}
              type="email"
              value={formData.email}
              onChange={(e) => handleChange('email', e.target.value)}
              error={!!validationErrors.email}
              helperText={validationErrors.email}
              required
              sx={{ mb: 3 }}
            />

            <FormControl fullWidth sx={{ mb: 3 }} error={!!validationErrors.reason}>
              <InputLabel>{t('unsubscribe.reasonLabel')}</InputLabel>
              <Select
                value={formData.reason}
                onChange={(e) => handleChange('reason', e.target.value)}
                label={t('unsubscribe.reasonLabel')}
                required
              >
                <MenuItem value="">{t('unsubscribe.reasonPlaceholder')}</MenuItem>
                <MenuItem value="dont_want_emails">{t('unsubscribe.reasonOption1')}</MenuItem>
                <MenuItem value="too_many_emails">{t('unsubscribe.reasonOption2')}</MenuItem>
                <MenuItem value="not_relevant">{t('unsubscribe.reasonOption3')}</MenuItem>
                <MenuItem value="other">{t('unsubscribe.reasonOption4')}</MenuItem>
              </Select>
              {validationErrors.reason && (
                <Typography variant="caption" color="error" sx={{ mt: 0.5, ml: 2 }}>
                  {validationErrors.reason}
                </Typography>
              )}
            </FormControl>

            <TextField
              fullWidth
              label={t('unsubscribe.commentsLabel')}
              placeholder={t('unsubscribe.commentsPlaceholder')}
              multiline
              rows={4}
              value={formData.comments}
              onChange={(e) => handleChange('comments', e.target.value)}
              sx={{ mb: 3 }}
            />

            <Button
              type="submit"
              fullWidth
              variant="contained"
              size="large"
              disabled={loading}
              sx={{
                backgroundColor: '#d32f2f',
                py: 1.5,
                fontSize: '1rem',
                fontWeight: 'bold',
                '&:hover': {
                  backgroundColor: '#b71c1c',
                },
              }}
            >
              {loading ? (
                <CircularProgress size={24} sx={{ color: 'white' }} />
              ) : (
                t('unsubscribe.submitButton')
              )}
            </Button>
          </form>
        </Paper>
      </Container>
    </Box>
  )
}

export default Unsubscribe
