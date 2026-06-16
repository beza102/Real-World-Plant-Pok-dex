import { useState } from 'react'
import ImageUpload from './components/ImageUpload'
import PokedexCard from './components/PokedexCard'
import VoicePlayer from './components/VoicePlayer'
import { mockIdentifyPlant } from './services/mockData'
import './styles/App.css'

export default function App() {
  const [status, setStatus] = useState('idle')
  const [result, setResult] = useState(null)
  const [imageUrl, setImageUrl] = useState(null)
  const [errorMsg, setErrorMsg] = useState('')

  async function handleImageSelected(file) {
    setImageUrl(URL.createObjectURL(file))
    setStatus('loading')
    setResult(null)
    setErrorMsg('')

    try {
      const data = await mockIdentifyPlant(file)
      setResult(data)
      setStatus('result')
    } catch (err) {
      console.error(err)
      setErrorMsg(err.message || 'Something went wrong. Please try again.')
      setStatus('error')
    }
  }

  function handleReset() {
    setStatus('idle')
    setResult(null)
    setImageUrl(null)
    setErrorMsg('')
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>Plant Pokédex</h1>
        <p className="app-subtitle">Point at a plant. We'll tell you everything.</p>
      </header>

      <main className="app-main">
        <ImageUpload
          onImageSelected={handleImageSelected}
          disabled={status === 'loading'}
        />

        {status === 'loading' && (
          <div className="status-loading">
            <p>Identifying plant…</p>
          </div>
        )}

        {status === 'error' && (
          <div className="status-error">
            <p>{errorMsg}</p>
            <button onClick={handleReset}>Try again</button>
          </div>
        )}

        {status === 'result' && result && (
          <>
            <PokedexCard result={result} imageUrl={imageUrl} />
            <VoicePlayer text={result.entry} />
            <button className="reset-btn" onClick={handleReset}>
              Scan another plant
            </button>
          </>
        )}
      </main>
    </div>
  )
}