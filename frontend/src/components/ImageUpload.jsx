export default function ImageUpload({ onImageSelected, disabled }) {
  function handleFileChange(e) {
    const file = e.target.files?.[0]
    if (file) onImageSelected(file)
  }

  return (
    <div className="upload-placeholder">
      <p>Image upload coming soon</p>
      <input
        type="file"
        accept="image/jpeg,image/png"
        onChange={handleFileChange}
        disabled={disabled}
      />
    </div>
  )
}