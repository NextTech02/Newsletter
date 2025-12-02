import { createContext, useContext, useState, useEffect } from 'react'
import { authAPI } from '../services/api'

const AuthContext = createContext()

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [token, setToken] = useState(() => localStorage.getItem('token'))

  useEffect(() => {
    // Verificar se há token salvo e validá-lo
    const validateToken = async () => {
      const savedToken = localStorage.getItem('token')

      if (savedToken) {
        try {
          const response = await authAPI.validate()
          if (response.valid) {
            setUser(response.user)
            setToken(savedToken)
          } else {
            // Token inválido
            localStorage.removeItem('token')
            setToken(null)
            setUser(null)
          }
        } catch (error) {
          console.error('Erro ao validar token:', error)
          localStorage.removeItem('token')
          setToken(null)
          setUser(null)
        }
      }

      setLoading(false)
    }

    validateToken()
  }, [])

  const login = async (username, password) => {
    try {
      const response = await authAPI.login(username, password)

      // Salvar token
      localStorage.setItem('token', response.access_token)
      setToken(response.access_token)
      setUser(response.user)

      return { success: true }
    } catch (error) {
      console.error('Erro no login:', error)
      return {
        success: false,
        error: error.response?.data?.detail || 'Erro ao fazer login'
      }
    }
  }

  const logout = () => {
    localStorage.removeItem('token')
    setToken(null)
    setUser(null)
  }

  const value = {
    user,
    token,
    loading,
    isAuthenticated: !!user,
    login,
    logout,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
