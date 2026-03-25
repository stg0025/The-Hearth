import { useState } from 'react'
import { submitCheckin } from '../api/client'
import styles from './CheckinPage.module.css'

const EMOTIONS = [
  'admiration', 'adoration', 'aesthetic appreciation', 'amusement',
  'anger', 'anxiety', 'awe', 'awkwardness', 'boredom', 'calmness',
  'confusion', 'craving', 'disgust', 'empathic pain', 'entrancement',
  'excitement', 'fear', 'horror', 'interest', 'joy', 'nostalgia',
  'relief', 'romance', 'sadness', 'satisfaction', 'sexual desire', 'surprise'
]

const NEEDS = [
  'connection', 'intimacy', 'belonging', 'to be understood', 'to be seen',
  'safety', 'stability', 'control',
  'recognition', 'autonomy', 'competence', 'purpose', 'honesty',
  'rest', 'comfort', 'relief from pain', 'peace',
  'stimulation', 'excitement', 'novelty', 'play', 'beauty',
  'meaning', 'growth', 'contribution'
]

function toggle(arr, val) {
  return arr.includes(val) ? arr.filter((v) => v !== val) : [...arr, val]
}

const STEP_SAFETY   = 'safety'
const STEP_READY    = 'ready'
const STEP_EMOTIONS = 'emotions'
const STEP_NEEDS    = 'needs'
const STEP_RELAPSE  = 'relapse'
const STEP_NOTES    = 'notes'
const STEP_DONE     = 'done'

export default function CheckinPage() {
  const [step, setStep]         = useState(STEP_READY)
  const [emotions, setEmotions] = useState([])
  const [needs, setNeeds]       = useState([])
  const [relapsed, setRelapsed] = useState(null)
  const [notes, setNotes]       = useState('')
  const [error, setError]       = useState(null)
  const [loading, setLoading]   = useState(false)
  const [emotionErr, setEmotionErr] = useState(false)
  const [needErr, setNeedErr]       = useState(false)

  const submit = async () => {
    setLoading(true)
    setError(null)
    try {
      await submitCheckin({
        emotion: emotions.join(', '),
        unmet_need: needs.join(', '),
        relapsed: relapsed === true,
        notes
      })
      setStep(STEP_DONE)
    } catch (err) {
      setError(err?.response?.data?.detail ?? 'Submission failed.')
    } finally {
      setLoading(false)
    }
  }

  // ── Safety ────────────────────────────────────────────────────────────────
  if (step === STEP_SAFETY) {
    return (
      <div className={styles.page}>
        <div className={styles.safetyBox}>
          <div className={styles.safetyBorder} />
          <p className={styles.safetyText}>
            This tool is for behavioral patterns only.<br />
            If you are experiencing thoughts of self-harm,
            trauma responses, or crisis — contact a professional.
          </p>
          <p className={styles.crisisLine}>
            Crisis line: <strong>988</strong> (US) &nbsp;|&nbsp; Text <strong>HOME</strong> to <strong>741741</strong>
          </p>
          <div className={styles.safetyBorder} />
          <button className={styles.submit} onClick={() => setStep(STEP_READY)}>
            I understand — continue
          </button>
        </div>
      </div>
    )
  }

  // ── Ready gate ────────────────────────────────────────────────────────────
  if (step === STEP_READY) {
    return (
      <div className={styles.page}>
        <div className={styles.readyBox}>
          <p className={styles.readyText}>
            It's time to check in for the day. Take your time.
          </p>
          <button className={styles.submit} onClick={() => setStep(STEP_EMOTIONS)}>
            I'm ready
          </button>
        </div>
      </div>
    )
  }

  // ── Emotions ──────────────────────────────────────────────────────────────
  if (step === STEP_EMOTIONS) {
    return (
      <div className={styles.page}>
        <h2 className={styles.heading}>How are you doing today?</h2>
        <p className={styles.sub}>Select any emotions you're feeling today.</p>

        {emotionErr && (
          <p className={styles.warn}>Pick at least one — there's no wrong answer.</p>
        )}

        <div className={styles.pills}>
          {EMOTIONS.map((e) => (
            <button
              key={e}
              type="button"
              className={`${styles.pill} ${emotions.includes(e) ? styles.pillActive : ''}`}
              onClick={() => { setEmotions(toggle(emotions, e)); setEmotionErr(false) }}
            >
              {e}
            </button>
          ))}
        </div>

        <button
          className={styles.submit}
          onClick={() => {
            if (emotions.length === 0) { setEmotionErr(true); return }
            setStep(STEP_NEEDS)
          }}
        >
          next
        </button>
      </div>
    )
  }

  // ── Needs ─────────────────────────────────────────────────────────────────
  if (step === STEP_NEEDS) {
    return (
      <div className={styles.page}>
        <h2 className={styles.heading}>What feels unmet right now?</h2>
        <p className={styles.sub}>Select as many as feel true.</p>

        {needErr && (
          <p className={styles.warn}>Pick at least one need from the list.</p>
        )}

        <div className={styles.pills}>
          {NEEDS.map((n) => (
            <button
              key={n}
              type="button"
              className={`${styles.pill} ${needs.includes(n) ? styles.pillActive : ''}`}
              onClick={() => { setNeeds(toggle(needs, n)); setNeedErr(false) }}
            >
              {n}
            </button>
          ))}
        </div>

        <div className={styles.navRow}>
          <button className={styles.backBtn} onClick={() => setStep(STEP_EMOTIONS)}>back</button>
          <button
            className={styles.submit}
            onClick={() => {
              if (needs.length === 0) { setNeedErr(true); return }
              setStep(STEP_RELAPSE)
            }}
          >
            next
          </button>
        </div>
      </div>
    )
  }

  // ── Relapse ───────────────────────────────────────────────────────────────
  if (step === STEP_RELAPSE) {
    return (
      <div className={styles.page}>
        <h2 className={styles.heading}>Did you relapse today?</h2>

        <div className={styles.relapseToggle}>
          <button
            type="button"
            className={`${styles.relapseBtn} ${relapsed === false ? styles.relapseBtnActive : ''}`}
            onClick={() => setRelapsed(false)}
          >
            no
          </button>
          <button
            type="button"
            className={`${styles.relapseBtn} ${relapsed === true ? styles.relapseBtnDanger : ''}`}
            onClick={() => setRelapsed(true)}
          >
            yes
          </button>
        </div>

        <div className={styles.navRow}>
          <button className={styles.backBtn} onClick={() => setStep(STEP_NEEDS)}>back</button>
          <button
            className={styles.submit}
            disabled={relapsed === null}
            onClick={() => setStep(STEP_NOTES)}
          >
            next
          </button>
        </div>
      </div>
    )
  }

  // ── Notes ─────────────────────────────────────────────────────────────────
  if (step === STEP_NOTES) {
    return (
      <div className={styles.page}>
        <h2 className={styles.heading}>Anything else you want to note?</h2>
        <p className={styles.sub}>You can always press Enter to skip.</p>

        <textarea
          rows={5}
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          placeholder="Optional..."
          className={styles.textarea}
        />

        {error && <p className={styles.error}>{error}</p>}

        <div className={styles.navRow}>
          <button className={styles.backBtn} onClick={() => setStep(STEP_RELAPSE)}>back</button>
          <button className={styles.submit} disabled={loading} onClick={submit}>
            {loading ? '...' : 'submit check-in'}
          </button>
        </div>
      </div>
    )
  }

  // ── Done ──────────────────────────────────────────────────────────────────
  if (step === STEP_DONE) {
    return (
      <div className={styles.page}>
        <div className={styles.done}>
          <p className={styles.doneTitle}>Thanks for checking in. Even checking in is a win.</p>
          <p className={styles.doneSub}>
            You named <em>{emotions.join(', ')}</em> and unmet needs for <em>{needs.join(', ')}</em>.
            {relapsed && <span className={styles.relapseNote}> Relapse logged.</span>}
          </p>
          <button className={styles.reset} onClick={() => {
            setStep(STEP_READY)
            setEmotions([])
            setNeeds([])
            setRelapsed(null)
            setNotes('')
            setError(null)
          }}>
            another check-in
          </button>
        </div>
      </div>
    )
  }

  return null
}
