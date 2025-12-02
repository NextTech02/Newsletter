import { useState, useEffect } from 'react'
import {
  Box, Typography, Paper, Button, TextField, Dialog, DialogTitle,
  DialogContent, DialogActions, Table, TableBody, TableCell,
  TableContainer, TableHead, TableRow, IconButton, Snackbar, Alert, Chip
} from '@mui/material'
import { Add as AddIcon, Delete as DeleteIcon, Refresh as RefreshIcon } from '@mui/icons-material'
import { leadsAPI } from '../services/api'
import { useLanguage } from '../contexts/LanguageContext'
import { useTranslation } from '../translations/translations'

function Leads() {
  const [leads, setLeads] = useState([])
  const [loading, setLoading] = useState(false)
  const [openDialog, setOpenDialog] = useState(false)
  const [newLead, setNewLead] = useState({ email: '', nome: '' })
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' })
  const { language } = useLanguage()
  const t = useTranslation(language)

  useEffect(() => {
    loadLeads()
  }, [])

  const loadLeads = async () => {
    setLoading(true)
    try {
      const data = await leadsAPI.getAll()
      setLeads(data.leads)
    } catch (error) {
      showSnackbar(t('leads.errorLoad'), 'error')
    } finally {
      setLoading(false)
    }
  }

  const handleAddLead = async () => {
    try {
      await leadsAPI.create(newLead)
      showSnackbar(t('leads.successAdd'), 'success')
      setOpenDialog(false)
      setNewLead({ email: '', nome: '' })
      loadLeads()
    } catch (error) {
      showSnackbar(t('leads.errorAdd'), 'error')
    }
  }

  const handleDeleteLead = async (id) => {
    if (window.confirm(t('leads.confirmRemove'))) {
      try {
        await leadsAPI.delete(id)
        showSnackbar(t('leads.successRemove'), 'success')
        loadLeads()
      } catch (error) {
        showSnackbar(t('leads.errorRemove'), 'error')
      }
    }
  }

  const showSnackbar = (message, severity) => {
    setSnackbar({ open: true, message, severity })
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
          {t('leads.title')}
        </Typography>
        <Box>
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={loadLeads}
            sx={{ mr: 2 }}
            disabled={loading}
          >
            {t('leads.refresh')}
          </Button>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setOpenDialog(true)}
          >
            {t('leads.addLead')}
          </Button>
        </Box>
      </Box>

      <Paper elevation={0} sx={{ borderRadius: 2, overflow: 'hidden' }}>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow sx={{ backgroundColor: '#32373c' }}>
                <TableCell sx={{ color: 'white', fontWeight: 'bold' }}>{t('leads.id')}</TableCell>
                <TableCell sx={{ color: 'white', fontWeight: 'bold' }}>{t('leads.email')}</TableCell>
                <TableCell sx={{ color: 'white', fontWeight: 'bold' }}>{t('leads.name')}</TableCell>
                <TableCell sx={{ color: 'white', fontWeight: 'bold' }}>{t('leads.status')}</TableCell>
                <TableCell align="center" sx={{ color: 'white', fontWeight: 'bold' }}>{t('leads.actions')}</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {leads.map((lead) => (
                <TableRow
                  key={lead.id}
                  sx={{
                    '&:hover': {
                      backgroundColor: 'rgba(0, 166, 188, 0.05)'
                    }
                  }}
                >
                  <TableCell>{lead.id}</TableCell>
                  <TableCell sx={{ fontWeight: 500 }}>{lead.email}</TableCell>
                  <TableCell>{lead.nome || '-'}</TableCell>
                  <TableCell>
                    <Chip
                      label={lead.subscribed ? t('leads.subscribed') : t('leads.inactive')}
                      sx={{
                        backgroundColor: lead.subscribed ? '#00a6bc' : '#e0e0e0',
                        color: lead.subscribed ? 'white' : '#666',
                        fontWeight: 600
                      }}
                      size="small"
                    />
                  </TableCell>
                  <TableCell align="center">
                    <IconButton
                      onClick={() => handleDeleteLead(lead.id)}
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
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>

      {/* Dialog para adicionar lead */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>{t('leads.dialogTitle')}</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label={t('leads.emailLabel')}
            type="email"
            value={newLead.email}
            onChange={(e) => setNewLead({ ...newLead, email: e.target.value })}
            margin="normal"
            required
          />
          <TextField
            fullWidth
            label={t('leads.nameLabel')}
            value={newLead.nome}
            onChange={(e) => setNewLead({ ...newLead, nome: e.target.value })}
            margin="normal"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>{t('leads.cancel')}</Button>
          <Button
            onClick={handleAddLead}
            variant="contained"
            disabled={!newLead.email}
          >
            {t('leads.add')}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Snackbar para mensagens */}
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

export default Leads
