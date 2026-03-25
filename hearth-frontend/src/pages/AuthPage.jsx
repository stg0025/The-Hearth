import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import styles from './AuthPage.module.css'

export default function AuthPage() {
  const [mode, setMode]           = useState('login')
  const [name, setName]           = useState('')
  const [addiction, setAddiction] = useState('')
  const [password, setPassword]   = useState('')
  const [error, setError]         = useState(null)
  const [loading, setLoading]     = useState(false)

  const { login, register } = useAuth()
  const navigate = useNavigate()

  const handle = async (e) => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      if (mode === 'login') {
        await login(name, password)
        navigate('/dashboard')
      } else {
        await register(name, addiction, password)
        setMode('login')
        setPassword('')
        setAddiction('')
      }
    } catch (err) {
      setError(err?.response?.data?.detail ?? 'Something went wrong.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={styles.page}>
      <div className={styles.card}>
        <div className={styles.header}>
          <span className={styles.flame}>&#9632;</span>
          <h1 className={styles.title}>The Hearth</h1>
          <p className={styles.sub}>
            {mode === 'login' ? 'Welcome back.' : 'Create an account.'}
          </p>
        </div>

        <form className={styles.form} onSubmit={handle}>
          <div className={styles.field}>
            <label className={styles.label}>name</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              autoComplete="username"
              required
            />
          </div>

          {mode === 'register' && (
            <div className={styles.field}>
              <label className={styles.label}>what are you working on?</label>
              <input
                type="text"
                value={addiction}
                onChange={(e) => setAddiction(e.target.value)}
                placeholder="e.g. alcohol, gambling, social media"
                required
              />
            </div>
          )}

          <div className={styles.field}>
            <label className={styles.label}>password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete={mode === 'login' ? 'current-password' : 'new-password'}
              required
            />
          </div>

          {error && <p className={styles.error}>{error}</p>}

          <button className={styles.submit} type="submit" disabled={loading}>
            {loading ? '...' : mode === 'login' ? 'sign in' : 'create account'}
          </button>
        </form>

        <p className={styles.toggle}>
          {mode === 'login' ? (
            <>no account?{' '}
              <button className={styles.link} onClick={() => { setMode('register'); setError(null) }}>
                register
              </button>
            </>
          ) : (
            <>already registered?{' '}
              <button className={styles.link} onClick={() => { setMode('login'); setError(null) }}>
                sign in
              </button>
            </>
          )}
        </p>
      </div>
    </div>
  )
}
