import { createContext, useContext, useState, useEffect } from 'react'
import { login as apiLogin, register as apiRegister } from '../api/client'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser]     = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const stored = localStorage.getItem('hearth_user')
    if (stored) setUser(JSON.parse(stored))
    setLoading(false)
  }, [])

  const login = async (name, password) => {
    const res = await apiLogin(name, password)
    const token = res.data.token ?? null
    if (token) localStorage.setItem('hearth_token', token)
    const userData = { username: name, user_id: res.data.user_id, safetyAcked: false }
    localStorage.setItem('hearth_user', JSON.stringify(userData))
    setUser(userData)
    return res
  }

  const register = async (name, addiction, password) => {
    const res = await apiRegister(name, addiction, password)
    return res
  }

  const ackSafety = () => {
    const updated = { ...user, safetyAcked: true }
    localStorage.setItem('hearth_user', JSON.stringify(updated))
    setUser(updated)
  }

  const logout = () => {
    localStorage.removeItem('hearth_token')
    localStorage.removeItem('hearth_user')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, login, register, logout, ackSafety, loading }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
