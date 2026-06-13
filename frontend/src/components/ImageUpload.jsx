import { useRef, useState } from 'react'
import '../styles/ImageUpload.css'

export default function ImageUpload({ onImageSelected, disabled }) {
  const [isDragging, setIsDragging] = useState(false)
  const inputRef = useRef(null)

  function handleFile(file) {
    if (!file) return
    if (!['image/jpeg', 'image/png'].includes(file.type)) {
      alert('Please upload a JPG or PNG image.')
      return
    }
    if (file.size > 52428800) {
      alert('Image is too large. Max size is 50 MB.')
      return
    }
    onImageSelected(file)
  }

  function handleFileChange(e) {
    handleFile(e.target.files?.[0])
  }

  function handleDrop(e) {
    e.preventDefault()
    setIsDragging(false)
    handleFile(e.dataTransfer.files?.[0])
  }

  function handleDragOver(e) {
    e.preventDefault()
    setIsDragging(true)
  }

  function handleDragLeave() {
    setIsDragging(false)
  }

  function handleClick() {
    inputRef.current?.click()
  }

  return (
    <div
      className={`upload-zone ${isDragging ? 'upload-zone--dragging' : ''} ${disabled ? 'upload-zone--disabled' : ''}`}
      onClick={!disabled ? handleClick : undefined}
      onDrop={!disabled ? handleDrop : undefined}
      onDragOver={!disabled ? handleDragOver : undefined}
      onDragLeave={handleDragLeave}
      role="button"
      tabIndex={0}
      aria-label="Upload a plant photo"
    >
      <div className="upload-zone__icon">
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round">
          <path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/>
          <circle cx="12" cy="13" r="3"/>
        </svg>
      </div>
      <p className="upload-zone__title">Tap to scan a plant</p>
      <p className="upload-zone__subtitle">or drag and drop a photo here</p>
      <p className="upload-zone__hint">JPG or PNG · max 50 MB</p>

      <input
        ref={inputRef}
        type="file"
        accept="image/jpeg,image/png"
        capture="environment"
        onChange={handleFileChange}
        disabled={disabled}
        style={{ display: 'none' }}
      />
    </div>
  )
}