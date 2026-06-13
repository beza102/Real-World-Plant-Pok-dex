export default function VoicePlayer({ text }) {
  function speak() {
    if (!text || !window.speechSynthesis) return
    const utterance = new SpeechSynthesisUtterance(text)
    window.speechSynthesis.speak(utterance)
  }

  if (!text) return null

  return (
    <div className="voice-placeholder">
      <button onClick={speak}>Read entry aloud</button>
    </div>
  )
}