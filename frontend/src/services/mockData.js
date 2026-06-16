export const MOCK_RESULT = {
  scientific_name: 'Guzmania conifera',
  entry:
    'This striking bromeliad makes its home in the cloud forests of Ecuador and Peru, ' +
    'clinging to mossy branches high in the canopy. Remarkably, its vivid red cone is not ' +
    'a flower at all — it is a cluster of bracts that can stay colorful for up to six months ' +
    'after the true tiny flowers fade. Care Difficulty: Moderate — it needs bright indirect ' +
    'light and water poured directly into its central cup, not the soil.',
  model: 'gemini-2.5-flash',
}

export function mockIdentifyPlant(_imageFile) {
  return new Promise((resolve) => {
    setTimeout(() => resolve(MOCK_RESULT), 1800)
  })
}