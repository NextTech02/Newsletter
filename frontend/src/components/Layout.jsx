import { useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import {
  Box,
  Drawer,
  AppBar,
  Toolbar,
  List,
  Typography,
  Divider,
  IconButton,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Container,
  ToggleButtonGroup,
  ToggleButton,
  Button,
} from '@mui/material'
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  People as PeopleIcon,
  Email as EmailIcon,
  Group as GroupIcon,
  Logout as LogoutIcon,
} from '@mui/icons-material'
import { useLanguage } from '../contexts/LanguageContext'
import { useTranslation } from '../translations/translations'
import { useAuth } from '../contexts/AuthContext'

const drawerWidth = 240

function Layout({ children }) {
  const [mobileOpen, setMobileOpen] = useState(false)
  const navigate = useNavigate()
  const location = useLocation()
  const { language, changeLanguage } = useLanguage()
  const { logout, user } = useAuth()
  const t = useTranslation(language)

  const menuItems = [
    { text: t('menu.dashboard'), icon: <DashboardIcon />, path: '/dashboard' },
    { text: t('menu.leads'), icon: <PeopleIcon />, path: '/leads' },
    { text: t('menu.newsletter'), icon: <EmailIcon />, path: '/newsletter' },
    ...(user?.is_admin ? [{ text: t('menu.users'), icon: <GroupIcon />, path: '/users' }] : []),
  ]

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen)
  }

  const handleNavigation = (path) => {
    navigate(path)
    setMobileOpen(false)
  }

  const drawer = (
    <div>
      <Toolbar sx={{
        backgroundColor: '#32373c',
        minHeight: '100px !important',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        py: 2
      }}>
        <Box
          component="img"
          src="/assets/logo_fcp_branco-768x352.png"
          alt="Federación Colombiana de Póker"
          sx={{
            width: '85%',
            maxWidth: '200px',
            height: 'auto',
            objectFit: 'contain'
          }}
        />
      </Toolbar>
      <Divider />
      <List sx={{ pt: 2 }}>
        {menuItems.map((item) => (
          <ListItem key={item.text} disablePadding sx={{ mb: 0.5 }}>
            <ListItemButton
              selected={location.pathname === item.path}
              onClick={() => handleNavigation(item.path)}
              sx={{
                mx: 1,
                borderRadius: 1,
                '&.Mui-selected': {
                  backgroundColor: 'rgba(0, 166, 188, 0.1)',
                  borderLeft: '3px solid #00a6bc',
                  '& .MuiListItemIcon-root': {
                    color: '#00a6bc'
                  },
                  '& .MuiListItemText-primary': {
                    color: '#00a6bc',
                    fontWeight: 600
                  }
                }
              }}
            >
              <ListItemIcon sx={{ color: '#32373c' }}>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
      <Divider sx={{ mt: 'auto' }} />
      <Box sx={{ p: 2 }}>
        <Button
          fullWidth
          variant="outlined"
          startIcon={<LogoutIcon />}
          onClick={handleLogout}
          sx={{
            borderColor: '#d32f2f',
            color: '#d32f2f',
            '&:hover': {
              borderColor: '#b71c1c',
              backgroundColor: 'rgba(211, 47, 47, 0.05)',
            },
          }}
        >
          {t('menu.logout')}
        </Button>
      </Box>
    </div>
  )

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar
        position="fixed"
        sx={{
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
        }}
      >
        <Toolbar sx={{ display: 'flex', justifyContent: 'space-between' }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <IconButton
              color="inherit"
              edge="start"
              onClick={handleDrawerToggle}
              sx={{ mr: 2, display: { sm: 'none' } }}
            >
              <MenuIcon />
            </IconButton>
            <Typography variant="h6" noWrap component="div">
              Federación Colombiana de Póker
            </Typography>
          </Box>

          <ToggleButtonGroup
            value={language}
            exclusive
            onChange={(e, newLang) => newLang && changeLanguage(newLang)}
            size="small"
            sx={{
              '& .MuiToggleButton-root': {
                color: 'white',
                borderColor: 'rgba(255,255,255,0.3)',
                px: 2,
                py: 0.5,
                fontSize: '0.875rem',
                fontWeight: 600,
                '&.Mui-selected': {
                  backgroundColor: '#00a6bc',
                  color: 'white',
                  '&:hover': {
                    backgroundColor: '#008394',
                  }
                },
                '&:hover': {
                  backgroundColor: 'rgba(255,255,255,0.1)',
                }
              }
            }}
          >
            <ToggleButton value="pt">PT</ToggleButton>
            <ToggleButton value="es">ES</ToggleButton>
          </ToggleButtonGroup>
        </Toolbar>
      </AppBar>

      <Box
        component="nav"
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
      >
        {/* Mobile drawer */}
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true, // Better open performance on mobile.
          }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
        >
          {drawer}
        </Drawer>

        {/* Desktop drawer */}
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          minHeight: '100vh',
          backgroundColor: '#f5f5f5',
        }}
      >
        <Toolbar />
        <Container maxWidth="xl">
          {children}
        </Container>
      </Box>
    </Box>
  )
}

export default Layout
