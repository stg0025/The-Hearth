import axios from 'axios'

const client = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' }
})

// Attach token if present
client.interceptors.request.use((config) => {
  const token = localStorage.getItem('hearth_token')
  if (token) config.headers['Authorization'] = `Bearer ${token}`
  return config
})

// ── Auth ──────────────────────────────────────────────────────────────────────

export const register = (name, addiction, password) =>
  client.post('/register', { name, addiction, password })

export const login = (name, password) =>
  client.post('/login', { name, password })

const getUserId = () => {
  const u = localStorage.getItem('hearth_user')
  return u ? JSON.parse(u).user_id : null
}

// ── Check-in ──────────────────────────────────────────────────────────────────

export const submitCheckin = (data) =>
  client.post('/checkin', { user_id: getUserId(), ...data })

// ── Craving / Urge Surfing ────────────────────────────────────────────────────

export const submitCraving = (data) =>
  client.post('/craving', { user_id: getUserId(), ...data })

// ── Dashboard ─────────────────────────────────────────────────────────────────

export const fetchDashboard = () =>
  client.get('/dashboard')
