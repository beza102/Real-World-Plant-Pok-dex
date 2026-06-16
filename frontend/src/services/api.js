const BASE_URL = '/api'

/**
 * Send a plant image to the backend pipeline.
 * @param {File} imageFile
 * @returns {Promise<{ scientific_name: string, entry: string, model: string }>}
 */
export async function identifyPlant(imageFile) {
  const formData = new FormData()
  formData.append('file', imageFile)

  const response = await fetch(`${BASE_URL}/identify`, {
    method: 'POST',
    body: formData,
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || `Server error: ${response.status}`)
  }

  return response.json()
}