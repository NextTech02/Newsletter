import axios from 'axios'

// Use variável de ambiente ou localhost como fallback
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptor para adicionar token de autenticação
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// ============================================================================
// LEADS
// ============================================================================

export const leadsAPI = {
  // Buscar todos os leads
  getAll: async () => {
    const response = await api.get('/leads/')
    return response.data
  },

  // Buscar leads inscritos
  getSubscribed: async () => {
    const response = await api.get('/leads/subscribed')
    return response.data
  },

  // Criar novo lead
  create: async (leadData) => {
    const response = await api.post('/leads/', leadData)
    return response.data
  },

  // Deletar lead
  delete: async (leadId) => {
    const response = await api.delete(`/leads/${leadId}`)
    return response.data
  },

  // Cancelar inscrição
  unsubscribe: async (email) => {
    const response = await api.post('/leads/unsubscribe', null, {
      params: { email }
    })
    return response.data
  },
}

// ============================================================================
// NEWSLETTER
// ============================================================================

export const newsletterAPI = {
  // Gerar preview da newsletter
  preview: async (newsletterData) => {
    const response = await api.post('/newsletter/preview', newsletterData)
    return response.data
  },

  // Enviar newsletter
  send: async (emailRequest) => {
    const response = await api.post('/newsletter/send', emailRequest)
    return response.data
  },
}

// ============================================================================
// AUTH
// ============================================================================

export const authAPI = {
  // Login
  login: async (username, password) => {
    const response = await api.post('/auth/login', { username, password })
    return response.data
  },

  // Validar token
  validate: async () => {
    const response = await api.post('/auth/validate')
    return response.data
  },

  // Obter informações do usuário atual
  me: async () => {
    const response = await api.get('/auth/me')
    return response.data
  },
}

// ============================================================================
// USERS
// ============================================================================

export const usersAPI = {
  // Buscar todos os usuários
  getAll: async () => {
    const response = await api.get('/users/')
    return response.data
  },

  // Criar novo usuário
  create: async (userData) => {
    const response = await api.post('/users/', userData)
    return response.data
  },

  // Buscar usuário por ID
  getById: async (userId) => {
    const response = await api.get(`/users/${userId}`)
    return response.data
  },

  // Atualizar usuário
  update: async (userId, userData) => {
    const response = await api.put(`/users/${userId}`, userData)
    return response.data
  },

  // Deletar usuário
  delete: async (userId) => {
    const response = await api.delete(`/users/${userId}`)
    return response.data
  },
}

export default api
