import '../styles/PokedexCard.css'

export default function PokedexCard({ result, imageUrl }) {
  if (!result) return null

  return (
    <div className="pokedex-card">
      <div className="pokedex-card__header">
        <div>
          <p className="pokedex-card__label">Identified plant</p>
          <h2 className="pokedex-card__name">{result.scientific_name}</h2>
        </div>
      </div>

      {imageUrl && (
        <div className="pokedex-card__image-wrap">
          <img
            src={imageUrl}
            alt={result.scientific_name}
            className="pokedex-card__image"
          />
        </div>
      )}

      <div className="pokedex-card__entry">
        <p>{result.entry}</p>
      </div>
    </div>
  )
}