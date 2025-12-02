import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { ThemeProvider } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import fcpTheme from './theme'
import { LanguageProvider } from './contexts/LanguageContext'
import { AuthProvider } from './contexts/AuthContext'
import Layout from './components/Layout'
import ProtectedRoute from './components/ProtectedRoute'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Leads from './pages/Leads'
import Newsletter from './pages/Newsletter'
import Users from './pages/Users'
import Unsubscribe from './pages/Unsubscribe'

function App() {
  return (
    <ThemeProvider theme={fcpTheme}>
      <CssBaseline />
      <LanguageProvider>
        <AuthProvider>
          <Router>
            <Routes>
              {/* Rotas públicas */}
              <Route path="/login" element={<Login />} />
              <Route path="/unsubscribe" element={<Unsubscribe />} />

              {/* Rotas protegidas */}
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
              <Route
                path="/dashboard"
                element={
                  <ProtectedRoute>
                    <Layout>
                      <Dashboard />
                    </Layout>
                  </ProtectedRoute>
                }
              />
              <Route
                path="/leads"
                element={
                  <ProtectedRoute>
                    <Layout>
                      <Leads />
                    </Layout>
                  </ProtectedRoute>
                }
              />
              <Route
                path="/newsletter"
                element={
                  <ProtectedRoute>
                    <Layout>
                      <Newsletter />
                    </Layout>
                  </ProtectedRoute>
                }
              />
              <Route
                path="/users"
                element={
                  <ProtectedRoute>
                    <Layout>
                      <Users />
                    </Layout>
                  </ProtectedRoute>
                }
              />
            </Routes>
          </Router>
        </AuthProvider>
      </LanguageProvider>
    </ThemeProvider>
  )
}

export default App
