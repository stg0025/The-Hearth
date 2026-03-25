import { useState, useEffect, useRef } from 'react'
import { submitCraving } from '../api/client'
import styles from './CravingPage.module.css'

const EMOTIONS = [
  'admiration', 'adoration', 'aesthetic appreciation', 'amusement',
  'anger', 'anxiety', 'awe', 'awkwardness', 'boredom', 'calmness',
  'confusion', 'craving', 'disgust', 'empathic pain', 'entrancement',
  'excitement', 'fear', 'horror', 'interest', 'joy', 'nostalgia',
  'relief', 'romance', 'sadness', 'satisfaction', 'sexual desire', 'surprise'
]

const MAX_INTERVALS  = 6
const INTERVAL_MS    = 5 * 60 * 1000 // 5 minutes

const STEP_EMOTION   = 'emotion'
const STEP_SURFING   = 'surfing'
const STEP_WAITING   = 'waiting'
const STEP_DONE      = 'done'

export default function CravingPage() {
  const [step, setStep]               = useState(STEP_EMOTION)
  const [emotion, setEmotion]         = useState('')
  const [emotionErr, setEmotionErr]   = useState(false)
  const [intervalIdx, setIntervalIdx] = useState(0)       // 0-based, which interval we're on
  const [intensity, setIntensity]     = useState('')
  const [intensities, setIntensities] = useState([])
  const [inputErr, setInputErr]       = useState('')
  const [secondsLeft, setSecondsLeft] = useState(INTERVAL_MS / 1000)
  const [submitted, setSubmitted]     = useState(false)
  const [error, setError]             = useState(null)
  const [loading, setLoading]         = useState(false)

  const timerRef    = useRef(null)
  const countdownRef = useRef(null)

  // Countdown tick while waiting
  useEffect(() => {
    if (step === STEP_WAITING) {
      setSecondsLeft(INTERVAL_MS / 1000)

      countdownRef.current = setInterval(() => {
        setSecondsLeft((s) => {
          if (s <= 1) {
            clearInterval(countdownRef.current)
            return 0
          }
          return s - 1
        })
      }, 1000)

      timerRef.current = setTimeout(() => {
        setStep(STEP_SURFING)
      }, INTERVAL_MS)
    }
    return () => {
      clearTimeout(timerRef.current)
      clearInterval(countdownRef.current)
    }
  }, [step, intervalIdx])

  const formatTime = (s) => {
    const m = Math.floor(s / 60)
    const sec = s % 60
    return `${m}:${sec.toString().padStart(2, '0')}`
  }

  const logAndFinish = async (finalIntensities) => {
    setLoading(true)
    setError(null)
    try {
      await submitCraving({ emotion })
      setSubmitted(true)
      setStep(STEP_DONE)
    } catch (err) {
      setError(err?.response?.data?.detail ?? 'Failed to save session.')
    } finally {
      setLoading(false)
    }
  }

  const handleDone = () => {
    clearTimeout(timerRef.current)
    clearInterval(countdownRef.current)
    logAndFinish(intensities)
  }

  const handleIntensitySubmit = () => {
    const val = parseInt(intensity)
    if (isNaN(val) || val < 1 || val > 10) {
      setInputErr('Enter a number between 1 and 10.')
      return
    }
    setInputErr('')
    const updated = [...intensities, val]
    setIntensities(updated)
    setIntensity('')

    if (val === 1) {
      // Craving subsided
      logAndFinish(updated)
      return
    }

    const nextInterval = intervalIdx + 1
    if (nextInterval >= MAX_INTERVALS) {
      logAndFinish(updated)
      return
    }

    setIntervalIdx(nextInterval)
    setStep(STEP_WAITING)
  }

  // ── Emotion selection ─────────────────────────────────────────────────────
  if (step === STEP_EMOTION) {
    return (
      <div className={styles.page}>
        <h2 className={styles.heading}>Take a deep breath.</h2>
        <p className={styles.sub}>Let's surf this urge together. First, how are you feeling right now?</p>

        {emotionErr && <p className={styles.warn}>Pick one emotion to continue.</p>}

        <div className={styles.pills}>
          {EMOTIONS.map((e) => (
            <button
              key={e}
              type="button"
              className={`${styles.pill} ${emotion === e ? styles.pillActive : ''}`}
              onClick={() => { setEmotion(e); setEmotionErr(false) }}
            >
              {e}
            </button>
          ))}
        </div>

        <button
          className={styles.surfBtn}
          onClick={() => {
            if (!emotion) { setEmotionErr(true); return }
            setStep(STEP_SURFING)
          }}
        >
          start session
        </button>
      </div>
    )
  }

  // ── Rate intensity ────────────────────────────────────────────────────────
  if (step === STEP_SURFING) {
    return (
      <div className={styles.page}>
        <h2 className={styles.heading}>
          Interval {intervalIdx + 1} of {MAX_INTERVALS}
        </h2>
        <p className={styles.sub}>
          For the next few minutes, rate your craving intensity on a scale of 1 to 10.
          It's okay to feel this way. Stay present and ride it out.
        </p>

        <div className={styles.intensityRow}>
          <input
            type="number"
            min={1}
            max={10}
            value={intensity}
            onChange={(e) => { setIntensity(e.target.value); setInputErr('') }}
            className={styles.intensityInput}
            placeholder="1–10"
            autoFocus
          />
          <button className={styles.surfBtn} onClick={handleIntensitySubmit} disabled={loading}>
            {loading ? '...' : 'submit'}
          </button>
          <button className={styles.doneBtn} onClick={handleDone} disabled={loading}>
            done
          </button>
        </div>

        {inputErr && <p className={styles.warn}>{inputErr}</p>}
        {error && <p className={styles.error}>{error}</p>}

        {intensities.length > 0 && (
          <div className={styles.history}>
            {intensities.map((v, i) => (
              <span key={i} className={styles.historyItem}>
                interval {i + 1}: <strong>{v}</strong>
              </span>
            ))}
          </div>
        )}
      </div>
    )
  }

  // ── Waiting 5 minutes ─────────────────────────────────────────────────────
  if (step === STEP_WAITING) {
    return (
      <div className={styles.page}>
        <div className={styles.waitBox}>
          <p className={styles.waitLabel}>next check-in in</p>
          <p className={styles.countdown}>{formatTime(secondsLeft)}</p>
          <p className={styles.waitSub}>Hang in there. Check back in 5 minutes...</p>

          <div className={styles.waveMini}>
            <svg viewBox="0 0 200 40" xmlns="http://www.w3.org/2000/svg" className={styles.waveSvg}>
              <path d="M0 20 Q25 5 50 20 Q75 35 100 20 Q125 5 150 20 Q175 35 200 20"
                fill="none" stroke="var(--ember)" strokeWidth="1.5" opacity="0.5">
                <animate attributeName="d"
                  values="
                    M0 20 Q25 5 50 20 Q75 35 100 20 Q125 5 150 20 Q175 35 200 20;
                    M0 20 Q25 35 50 20 Q75 5 100 20 Q125 35 150 20 Q175 5 200 20;
                    M0 20 Q25 5 50 20 Q75 35 100 20 Q125 5 150 20 Q175 35 200 20"
                  dur="4s" repeatCount="indefinite" />
              </path>
            </svg>
          </div>

          <button className={styles.doneBtn} onClick={handleDone} disabled={loading}>
            i'm done — end session
          </button>
        </div>
      </div>
    )
  }

  // ── Done ──────────────────────────────────────────────────────────────────
  if (step === STEP_DONE) {
    const subsided = intensities.length > 0 && intensities[intensities.length - 1] === 1
    return (
      <div className={styles.page}>
        <div className={styles.done}>
          {subsided ? (
            <p className={styles.doneTitle}>
              Looks like the craving has mostly subsided. Great work riding that out.
            </p>
          ) : (
            <p className={styles.doneTitle}>
              Great job riding that out. Cravings are temporary — you have the strength to get through them.
            </p>
          )}
          <p className={styles.doneSub}>Session saved.</p>
          <button className={styles.reset} onClick={() => {
            setStep(STEP_EMOTION)
            setEmotion('')
            setIntervalIdx(0)
            setIntensity('')
            setIntensities([])
            setSubmitted(false)
            setError(null)
          }}>
            new session
          </button>
        </div>
      </div>
    )
  }

  return null
}
