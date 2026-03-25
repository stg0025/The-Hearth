import { useEffect, useState } from 'react'
import { fetchDashboard } from '../api/client'
import styles from './DashboardPage.module.css'

export default function DashboardPage() {
  const [data, setData]       = useState(null)
  const [error, setError]     = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboard()
      .then((res) => setData(res.data))
      .catch((err) => setError(err?.response?.data?.detail ?? 'Failed to load dashboard.'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className={styles.state}>loading...</div>
  if (error)   return <div className={styles.state + ' ' + styles.err}>{error}</div>

  const days     = data?.days ?? 0
  const sessions = data?.sessions ?? []
  const recent   = sessions.length > 0 ? sessions[sessions.length - 1] : null
  const relapses = sessions.filter((s) => s.relapsed).length

  return (
    <div className={styles.page}>
      <h2 className={styles.heading}>Dashboard</h2>

      <div className={styles.grid}>
        <div className={styles.card}>
          <span className={styles.cardLabel}>days tracked</span>
          <span className={styles.streakNum}>{days}</span>
          <span className={styles.streakUnit}>days</span>
        </div>

        <div className={styles.card}>
          <span className={styles.cardLabel}>total sessions</span>
          <span className={styles.streakNum}>{sessions.length}</span>
          <span className={styles.streakUnit}>check-ins</span>
        </div>

        <div className={styles.card}>
          <span className={styles.cardLabel}>logged relapses</span>
          <span className={`${styles.streakNum} ${relapses > 0 ? styles.relapse : ''}`}>
            {relapses}
          </span>
          <span className={styles.streakUnit}>total</span>
        </div>
      </div>

      {recent && (
        <div className={styles.recentCard}>
          <span className={styles.cardLabel}>most recent check-in</span>
          <div className={styles.recentGrid}>
            <div>
              <span className={styles.recentLabel}>emotion</span>
              <span className={styles.recentValue}>{recent.emotion ?? '—'}</span>
            </div>
            <div>
              <span className={styles.recentLabel}>unmet need</span>
              <span className={styles.recentValue}>{recent.unmet_need ?? '—'}</span>
            </div>
            <div>
              <span className={styles.recentLabel}>relapsed</span>
              <span className={`${styles.recentValue} ${recent.relapsed ? styles.relapse : styles.clean}`}>
                {recent.relapsed ? 'yes' : 'no'}
              </span>
            </div>
          </div>
          {recent.notes && (
            <p className={styles.notes}>{recent.notes}</p>
          )}
        </div>
      )}

      {sessions.length > 0 && (
        <div className={styles.chartCard}>
          <span className={styles.cardLabel}>session history</span>
          <div className={styles.sessionList}>
            {[...sessions].reverse().slice(0, 10).map((s, i) => (
              <div key={i} className={styles.sessionRow}>
                <span className={styles.sessionEmotion}>{s.emotion}</span>
                <span className={styles.sessionNeed}>{s.unmet_need}</span>
                {s.relapsed && <span className={styles.relapseBadge}>relapsed</span>}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
