import { useState, useEffect } from 'react'
import {
  Box, Typography, Paper, Button, TextField, Dialog, DialogTitle,
  DialogContent, DialogActions, Table, TableBody, TableCell,
  TableContainer, TableHead, TableRow, IconButton, Snackbar, Alert, Chip,
  FormControlLabel, Checkbox
} from '@mui/material'
import { Add as AddIcon, Delete as DeleteIcon, Refresh as RefreshIcon, AdminPanelSettings as AdminIcon, Edit as EditIcon } from '@mui/icons-material'
import { usersAPI } from '../services/api'
import { useLanguage } from '../contexts/LanguageContext'
import { useTranslation } from '../translations/translations'

function Users() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(false)
  const [openDialog, setOpenDialog] = useState(false)
  const [openEditDialog, setOpenEditDialog] = useState(false)
  const [editingUser, setEditingUser] = useState(null)
  const [newUser, setNewUser] = useState({
    username: '',
    email: '',
    password: '',
    full_name: '',
    is_admin: false,
  })
  const [editUser, setEditUser] = useState({
    email: '',
    full_name: '',
    password: '',
    is_admin: false,
  })
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' })
  const { language } = useLanguage()
  const t = useTranslation(language)

  useEffect(() => {
    loadUsers()
  }, [])

  const loadUsers = async () => {
    setLoading(true)
    try {
      const data = await usersAPI.getAll()
      setUsers(data.users)
    } catch (error) {
      showSnackbar(t('users.errorLoad'), 'error')
    } finally {
      setLoading(false)
    }
  }

  const handleAddUser = async () => {
    try {
      await usersAPI.create(newUser)
      showSnackbar(t('users.successAdd'), 'success')
      setOpenDialog(false)
      setNewUser({ username: '', email: '', password: '', full_name: '', is_admin: false })
      loadUsers()
    } catch (error) {
      const errorMsg = error.response?.data?.detail || t('users.errorAdd')
      showSnackbar(errorMsg, 'error')
    }
  }

  const handleOpenEditDialog = (user) => {
    setEditingUser(user)
    setEditUser({
      email: user.email,
      full_name: user.full_name || '',
      password: '',
      is_admin: user.is_admin,
    })
    setOpenEditDialog(true)
  }

  const handleUpdateUser = async () => {
    try {
      // Remover password do objeto se estiver vazio
      const updateData = { ...editUser }
      if (!updateData.password) {
        delete updateData.password
      }

      await usersAPI.update(editingUser.id, updateData)
      showSnackbar(t('users.successEdit'), 'success')
      setOpenEditDialog(false)
      setEditingUser(null)
      setEditUser({ email: '', full_name: '', password: '', is_admin: false })
      loadUsers()
    } catch (error) {
      const errorMsg = error.response?.data?.detail || t('users.errorEdit')
      showSnackbar(errorMsg, 'error')
    }
  }

  const handleDeleteUser = async (id) => {
    if (window.confirm(t('users.confirmRemove'))) {
      try {
        await usersAPI.delete(id)
        showSnackbar(t('users.successRemove'), 'success')
        loadUsers()
      } catch (error) {
        const errorMsg = error.response?.data?.detail || t('users.errorRemove')
        showSnackbar(errorMsg, 'error')
      }
    }
  }

  const showSnackbar = (message, severity) => {
    setSnackbar({ open: true, message, severity })
  }

  const formatDate = (dateString) => {
    if (!dateString) return '-'
    return new Date(dateString).toLocaleDateString()
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
          {t('users.title')}
        </Typography>
        <Box>
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={loadUsers}
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
            {t('users.addUser')}
          </Button>
        </Box>
      </Box>

      <Paper elevation={0} sx={{ borderRadius: 2, overflow: 'hidden' }}>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow sx={{ backgroundColor: '#32373c' }}>
                <TableCell sx={{ color: 'white', fontWeight: 'bold' }}>{t('users.username')}</TableCell>
                <TableCell sx={{ color: 'white', fontWeight: 'bold' }}>{t('users.email')}</TableCell>
                <TableCell sx={{ color: 'white', fontWeight: 'bold' }}>{t('users.fullName')}</TableCell>
                <TableCell sx={{ color: 'white', fontWeight: 'bold' }}>{t('leads.status')}</TableCell>
                <TableCell sx={{ color: 'white', fontWeight: 'bold' }}>{t('users.admin')}</TableCell>
                <TableCell sx={{ color: 'white', fontWeight: 'bold' }}>{t('users.createdAt')}</TableCell>
                <TableCell align="center" sx={{ color: 'white', fontWeight: 'bold' }}>{t('users.actions')}</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {users.map((user) => (
                <TableRow
                  key={user.id}
                  sx={{
                    '&:hover': {
                      backgroundColor: 'rgba(0, 166, 188, 0.05)'
                    }
                  }}
                >
                  <TableCell sx={{ fontWeight: 600 }}>{user.username}</TableCell>
                  <TableCell>{user.email}</TableCell>
                  <TableCell>{user.full_name || '-'}</TableCell>
                  <TableCell>
                    <Chip
                      label={user.active ? t('users.active') : t('users.inactive')}
                      sx={{
                        backgroundColor: user.active ? '#00a6bc' : '#e0e0e0',
                        color: user.active ? 'white' : '#666',
                        fontWeight: 600
                      }}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    {user.is_admin && (
                      <Chip
                        icon={<AdminIcon />}
                        label={t('users.admin')}
                        sx={{
                          backgroundColor: '#ff9800',
                          color: 'white',
                          fontWeight: 600
                        }}
                        size="small"
                      />
                    )}
                  </TableCell>
                  <TableCell>{formatDate(user.created_at)}</TableCell>
                  <TableCell align="center">
                    <IconButton
                      onClick={() => handleOpenEditDialog(user)}
                      size="small"
                      sx={{
                        color: '#00a6bc',
                        mr: 1,
                        '&:hover': {
                          backgroundColor: 'rgba(0, 166, 188, 0.1)'
                        }
                      }}
                    >
                      <EditIcon />
                    </IconButton>
                    <IconButton
                      onClick={() => handleDeleteUser(user.id)}
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

      {/* Dialog para adicionar usuário */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>{t('users.dialogTitle')}</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label={t('users.usernameLabel')}
            value={newUser.username}
            onChange={(e) => setNewUser({ ...newUser, username: e.target.value })}
            margin="normal"
            required
          />
          <TextField
            fullWidth
            label={t('users.emailLabel')}
            type="email"
            value={newUser.email}
            onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
            margin="normal"
            required
          />
          <TextField
            fullWidth
            label={t('users.passwordLabel')}
            type="password"
            value={newUser.password}
            onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
            margin="normal"
            required
          />
          <TextField
            fullWidth
            label={t('users.fullNameLabel')}
            value={newUser.full_name}
            onChange={(e) => setNewUser({ ...newUser, full_name: e.target.value })}
            margin="normal"
          />
          <FormControlLabel
            control={
              <Checkbox
                checked={newUser.is_admin}
                onChange={(e) => setNewUser({ ...newUser, is_admin: e.target.checked })}
                sx={{
                  color: '#00a6bc',
                  '&.Mui-checked': {
                    color: '#00a6bc',
                  },
                }}
              />
            }
            label={t('users.isAdmin')}
            sx={{ mt: 2 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>{t('users.cancel')}</Button>
          <Button
            onClick={handleAddUser}
            variant="contained"
            disabled={!newUser.username || !newUser.email || !newUser.password}
          >
            {t('users.add')}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Dialog para editar usuário */}
      <Dialog open={openEditDialog} onClose={() => setOpenEditDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>{t('users.editDialogTitle')}</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label={t('users.usernameLabel')}
            value={editingUser?.username || ''}
            margin="normal"
            disabled
            helperText="O nome de usuário não pode ser alterado"
          />
          <TextField
            fullWidth
            label={t('users.emailLabel')}
            type="email"
            value={editUser.email}
            onChange={(e) => setEditUser({ ...editUser, email: e.target.value })}
            margin="normal"
            required
          />
          <TextField
            fullWidth
            label={t('users.fullNameLabel')}
            value={editUser.full_name}
            onChange={(e) => setEditUser({ ...editUser, full_name: e.target.value })}
            margin="normal"
          />
          <TextField
            fullWidth
            label={t('users.newPasswordLabel')}
            type="password"
            value={editUser.password}
            onChange={(e) => setEditUser({ ...editUser, password: e.target.value })}
            margin="normal"
            helperText="Deixe em branco para manter a senha atual"
          />
          <FormControlLabel
            control={
              <Checkbox
                checked={editUser.is_admin}
                onChange={(e) => setEditUser({ ...editUser, is_admin: e.target.checked })}
                sx={{
                  color: '#00a6bc',
                  '&.Mui-checked': {
                    color: '#00a6bc',
                  },
                }}
              />
            }
            label={t('users.isAdmin')}
            sx={{ mt: 2 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenEditDialog(false)}>{t('users.cancel')}</Button>
          <Button
            onClick={handleUpdateUser}
            variant="contained"
            disabled={!editUser.email}
          >
            {t('users.save')}
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

export default Users
