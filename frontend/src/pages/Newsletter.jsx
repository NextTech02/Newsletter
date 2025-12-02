import { useState } from 'react'
import {
  Box, Typography, Paper, Grid, TextField, Button, Card, CardContent,
  IconButton, Divider, Dialog, DialogTitle, DialogContent, Snackbar, Alert, CircularProgress
} from '@mui/material'
import {
  Add as AddIcon, Delete as DeleteIcon, Preview as PreviewIcon,
  Send as SendIcon
} from '@mui/icons-material'
import { newsletterAPI } from '../services/api'
import { useLanguage } from '../contexts/LanguageContext'
import { useTranslation } from '../translations/translations'

function Newsletter() {
  const [subject, setSubject] = useState('')
  const [newsItems, setNewsItems] = useState([{ title: '', content: '' }])
  const [previewHtml, setPreviewHtml] = useState('')
  const [openPreview, setOpenPreview] = useState(false)
  const [loading, setLoading] = useState(false)
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' })
  const { language } = useLanguage()
  const t = useTranslation(language)

  const addNewsItem = () => {
    setNewsItems([...newsItems, { title: '', content: '' }])
  }

  const removeNewsItem = (index) => {
    const updated = newsItems.filter((_, i) => i !== index)
    setNewsItems(updated)
  }

  const updateNewsItem = (index, field, value) => {
    const updated = [...newsItems]
    updated[index][field] = value
    setNewsItems(updated)
  }

  const handlePreview = async () => {
    if (!subject || newsItems.some(item => !item.title || !item.content)) {
      showSnackbar(`${t('newsletter.fillAllFields')} ${t('newsletter.beforePreview')}`, 'warning')
      return
    }

    setLoading(true)
    try {
      const response = await newsletterAPI.preview({
        subject,
        news_items: newsItems,
        theme: 'federacion_poker'
      })
      setPreviewHtml(response.html)
      setOpenPreview(true)
    } catch (error) {
      showSnackbar(t('newsletter.errorPreview'), 'error')
    } finally {
      setLoading(false)
    }
  }

  const handleSend = async (isTest = false) => {
    if (!subject || newsItems.some(item => !item.title || !item.content)) {
      showSnackbar(`${t('newsletter.fillAllFields')} ${t('newsletter.beforeSend')}`, 'warning')
      return
    }

    if (!isTest && !window.confirm(t('newsletter.confirmSend'))) {
      return
    }

    setLoading(true)
    try {
      const previewResponse = await newsletterAPI.preview({
        subject,
        news_items: newsItems,
        theme: 'federacion_poker'
      })

      const sendResponse = await newsletterAPI.send({
        subject,
        html_content: previewResponse.html,
        is_test: isTest
      })

      if (sendResponse.success) {
        showSnackbar(
          isTest ? t('newsletter.testSent') : `${t('newsletter.sentSuccess')} ${sendResponse.total_sent} ${t('newsletter.emailsSent')}`,
          'success'
        )
      } else {
        showSnackbar(sendResponse.message, 'error')
      }
    } catch (error) {
      showSnackbar(t('newsletter.errorSend'), 'error')
    } finally {
      setLoading(false)
    }
  }

  const showSnackbar = (message, severity) => {
    setSnackbar({ open: true, message, severity })
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ fontWeight: 'bold', mb: 3 }}>
        {t('newsletter.title')}
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper
            elevation={0}
            sx={{
              p: 3,
              borderRadius: 2,
              border: '2px solid #00a6bc',
              backgroundColor: 'white'
            }}
          >
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold', color: '#32373c' }}>
              {t('newsletter.generalInfo')}
            </Typography>
            <TextField
              fullWidth
              label={t('newsletter.subject')}
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
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
                }
              }}
            />
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper elevation={0} sx={{ p: 3, borderRadius: 2 }}>
            <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
              <Typography variant="h6" sx={{ fontWeight: 'bold', color: '#32373c' }}>
                {t('newsletter.news')} ({newsItems.length})
              </Typography>
              <Button
                variant="outlined"
                startIcon={<AddIcon />}
                onClick={addNewsItem}
                sx={{
                  borderColor: '#00a6bc',
                  color: '#00a6bc',
                  '&:hover': {
                    borderColor: '#008394',
                    backgroundColor: 'rgba(0, 166, 188, 0.05)'
                  }
                }}
              >
                {t('newsletter.addNews')}
              </Button>
            </Box>

            {newsItems.map((item, index) => (
              <Card
                key={index}
                sx={{
                  mb: 2,
                  borderLeft: '4px solid #00a6bc',
                  borderRadius: 2
                }}
                elevation={0}
              >
                <CardContent>
                  <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                    <Typography
                      variant="subtitle1"
                      sx={{
                        fontWeight: 'bold',
                        color: '#00a6bc'
                      }}
                    >
                      {t('newsletter.newsCount')} {index + 1}
                    </Typography>
                    {newsItems.length > 1 && (
                      <IconButton
                        onClick={() => removeNewsItem(index)}
                        size="small"
                        sx={{
                          color: '#d32f2f',
                          '&:hover': {
                            backgroundColor: 'rgba(211, 47, 47, 0.1)'
                          }
                        }}
                      >
                        <DeleteIcon />
                      </IconButton>
                    )}
                  </Box>
                  <TextField
                    fullWidth
                    label={t('newsletter.titleLabel')}
                    value={item.title}
                    onChange={(e) => updateNewsItem(index, 'title', e.target.value)}
                    margin="normal"
                    required
                  />
                  <TextField
                    fullWidth
                    label={t('newsletter.contentLabel')}
                    value={item.content}
                    onChange={(e) => updateNewsItem(index, 'content', e.target.value)}
                    margin="normal"
                    multiline
                    rows={4}
                    required
                  />
                </CardContent>
              </Card>
            ))}
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
              {t('newsletter.actions')}
            </Typography>
            <Box display="flex" gap={2} flexWrap="wrap">
              <Button
                variant="outlined"
                startIcon={<PreviewIcon />}
                onClick={handlePreview}
                disabled={loading}
              >
                {t('newsletter.preview')}
              </Button>
              <Button
                variant="contained"
                color="secondary"
                startIcon={<SendIcon />}
                onClick={() => handleSend(true)}
                disabled={loading}
              >
                {t('newsletter.sendTest')}
              </Button>
              <Button
                variant="contained"
                startIcon={loading ? <CircularProgress size={20} /> : <SendIcon />}
                onClick={() => handleSend(false)}
                disabled={loading}
              >
                {t('newsletter.sendAll')}
              </Button>
            </Box>
          </Paper>
        </Grid>
      </Grid>

      {/* Dialog de Preview */}
      <Dialog open={openPreview} onClose={() => setOpenPreview(false)} maxWidth="md" fullWidth>
        <DialogTitle>{t('newsletter.previewTitle')}</DialogTitle>
        <DialogContent>
          <div dangerouslySetInnerHTML={{ __html: previewHtml }} />
        </DialogContent>
      </Dialog>

      {/* Snackbar */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={4000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
      >
        <Alert severity={snackbar.severity} sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  )
}

export default Newsletter
