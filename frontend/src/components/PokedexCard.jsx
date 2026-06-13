export default function PokedexCard({ result, imageUrl }) {
  if (!result) return null

  return (
    <div className="card-placeholder">
      {imageUrl && <img src={imageUrl} alt={result.scientific_name} width={120} />}
      <h2>{result.scientific_name}</h2>
      <p>{result.entry}</p>
      <small>Model: {result.model}</small>
    </div>
  )
}