import { useState, useEffect, useRef } from 'react'
import '../styles/VoicePlayer.css'

export default function VoicePlayer({ text }) {
  const [isSpeaking, setIsSpeaking] = useState(false)
  const [progress, setProgress] = useState(0)
  const utteranceRef = useRef(null)
  const intervalRef = useRef(null)
  const startTimeRef = useRef(null)
  const estimatedDuration = text ? text.length * 55 : 0

  useEffect(() => {
    return () => {
      window.speechSynthesis.cancel()
      clearInterval(intervalRef.current)
    }
  }, [])

  function startProgress() {
    startTimeRef.current = Date.now()
    intervalRef.current = setInterval(() => {
      const elapsed = Date.now() - startTimeRef.current
      const pct = Math.min((elapsed / estimatedDuration) * 100, 98)
      setProgress(pct)
    }, 100)
  }

  function stopProgress() {
    clearInterval(intervalRef.current)
    setProgress(0)
  }

  function handlePlay() {
    if (!text || !window.speechSynthesis) return

    const utterance = new SpeechSynthesisUtterance(text)
    utteranceRef.current = utterance

    utterance.onstart = () => {
      setIsSpeaking(true)
      startProgress()
    }
    utterance.onend = () => {
      setIsSpeaking(false)
      setProgress(100)
      setTimeout(() => setProgress(0), 400)
      clearInterval(intervalRef.current)
    }
    utterance.onerror = () => {
      setIsSpeaking(false)
      stopProgress()
    }

    window.speechSynthesis.speak(utterance)
  }

  function handleStop() {
    window.speechSynthesis.cancel()
    setIsSpeaking(false)
    stopProgress()
  }

  if (!text) return null

  return (
    <div className="voice-player">
      <button
        className={`voice-player__btn ${isSpeaking ? 'voice-player__btn--stop' : ''}`}
        onClick={isSpeaking ? handleStop : handlePlay}
        aria-label={isSpeaking ? 'Stop reading' : 'Read entry aloud'}
      >
        {isSpeaking ? (
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <rect x="6" y="6" width="12" height="12" rx="2" />
          </svg>
        ) : (
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <polygon points="5,3 19,12 5,21" />
          </svg>
        )}
        {isSpeaking ? 'Stop' : 'Read entry aloud'}
      </button>

      <div className="voice-player__progress-track">
        <div
          className="voice-player__progress-bar"
          style={{ width: `${progress}%` }}
        />
      </div>
    </div>
  )
}