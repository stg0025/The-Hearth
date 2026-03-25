import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import styles from './Layout.module.css'
import safetyStyles from './Safety.module.css'

const NAV = [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/checkin',   label: 'Check-In'  },
  { to: '/craving',   label: 'Urge Surf' },
]

function SafetyGate({ onAck }) {
  return (
    <div className={safetyStyles.page}>
      <div className={safetyStyles.box}>
        <div className={safetyStyles.border} />
        <p className={safetyStyles.text}>
          This tool is for behavioral patterns only.<br />
          If you are experiencing thoughts of self-harm,
          trauma responses, or crisis — contact a professional.
        </p>
        <p className={safetyStyles.crisis}>
          Crisis line: <strong>988</strong> (US) &nbsp;|&nbsp; Text <strong>HOME</strong> to <strong>741741</strong>
        </p>
        <div className={safetyStyles.border} />
        <button className={safetyStyles.btn} onClick={onAck}>
          I understand — continue
        </button>
      </div>
    </div>
  )
}

export default function Layout() {
  const { user, logout, ackSafety } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  if (!user?.safetyAcked) {
    return <SafetyGate onAck={ackSafety} />
  }

  return (
    <div className={styles.shell}>
      <aside className={styles.sidebar}>
        <div className={styles.brand}>
          <span className={styles.flame}>&#9632;</span>
          <span className={styles.brandName}>The Hearth</span>
        </div>

        <nav className={styles.nav}>
          {NAV.map(({ to, label }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `${styles.navLink} ${isActive ? styles.active : ''}`
              }
            >
              {label}
            </NavLink>
          ))}
        </nav>

        <div className={styles.userSection}>
          <span className={styles.username}>{user?.username}</span>
          <button className={styles.logoutBtn} onClick={handleLogout}>
            sign out
          </button>
        </div>
      </aside>

      <main className={styles.main}>
        <Outlet />
      </main>
    </div>
  )
}
