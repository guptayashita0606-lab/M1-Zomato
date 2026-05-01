import React, { useState, useEffect } from 'react'
import { Search, MapPin, DollarSign, Star, Loader2, AlertCircle, Utensils } from 'lucide-react'
import axios from 'axios'

interface Restaurant {
  name: string
  cuisines: string[]
  rating: number
  estimated_cost: string
  explanation: string
  restaurant_id?: string
}

interface RecommendationResponse {
  recommendations: Restaurant[]
  source: 'llm' | 'fallback' | 'no_candidates'
  total_candidates: number
  filtered_candidates: number
  request_id?: string
  telemetry?: any
}

interface MetaResponse {
  allowed_cities: string[]
  supported_budget_bands: string[]
  supported_cuisines: string[]
  rating_range: { min: number; max: number }
}

function App() {
  const [location, setLocation] = useState('')
  const [budgetBand, setBudgetBand] = useState<'low' | 'medium' | 'high'>('medium')
  const [cuisines, setCuisines] = useState<string[]>([])
  const [minimumRating, setMinimumRating] = useState(4.0)
  const [recommendations, setRecommendations] = useState<Restaurant[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [meta, setMeta] = useState<MetaResponse | null>(null)
  const [selectedCuisine, setSelectedCuisine] = useState('')

  useEffect(() => {
    fetchMetadata()
  }, [])

  const fetchMetadata = async () => {
    try {
      const response = await axios.get('/api/v1/meta')
      setMeta(response.data)
    } catch (err) {
      console.error('Failed to fetch metadata:', err)
    }
  }

  const handleCuisineAdd = (cuisine: string) => {
    if (cuisine && !cuisines.includes(cuisine)) {
      setCuisines([...cuisines, cuisine])
      setSelectedCuisine('')
    }
  }

  const handleCuisineRemove = (cuisine: string) => {
    setCuisines(cuisines.filter(c => c !== cuisine))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!location || cuisines.length === 0) {
      setError('Please provide location and at least one cuisine')
      return
    }

    setIsLoading(true)
    setError('')

    try {
      const response = await axios.post<RecommendationResponse>('/api/v1/recommendations', {
        location,
        budget_band: budgetBand,
        cuisines,
        minimum_rating: minimumRating,
        top_k: 5,
        source: 'hf'
      })

      setRecommendations(response.data.recommendations)
      
      if (response.data.recommendations.length === 0) {
        if (response.data.source === 'no_candidates') {
          setError('No restaurants found matching your criteria. Try adjusting your filters.')
        } else {
          setError('No recommendations available at the moment. Please try again.')
        }
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to get recommendations. Please try again.')
      setRecommendations([])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <header className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <Utensils className="w-8 h-8 text-orange-500 mr-2" />
            <h1 className="text-3xl font-bold text-gray-900">Restaurant Recommendations</h1>
          </div>
          <p className="text-gray-600">Discover great dining spots tailored to your preferences</p>
        </header>

        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <MapPin className="w-4 h-4 inline mr-1" />
                Location
              </label>
              <input
                type="text"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
                placeholder="Enter city or area..."
                required
              />
              {meta && (
                <p className="mt-1 text-xs text-gray-500">
                  Available cities: {meta.allowed_cities.slice(0, 5).join(', ')}
                  {meta.allowed_cities.length > 5 && '...'}
                </p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <DollarSign className="w-4 h-4 inline mr-1" />
                Budget
              </label>
              <div className="flex space-x-4">
                {['low', 'medium', 'high'].map((budget) => (
                  <label key={budget} className="flex items-center">
                    <input
                      type="radio"
                      value={budget}
                      checked={budgetBand === budget}
                      onChange={(e) => setBudgetBand(e.target.value as 'low' | 'medium' | 'high')}
                      className="mr-2"
                    />
                    <span className="capitalize">{budget}</span>
                  </label>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Cuisines
              </label>
              <div className="flex flex-wrap gap-2 mb-2">
                {cuisines.map((cuisine) => (
                  <span
                    key={cuisine}
                    className="bg-orange-100 text-orange-800 px-3 py-1 rounded-full text-sm flex items-center"
                  >
                    {cuisine}
                    <button
                      type="button"
                      onClick={() => handleCuisineRemove(cuisine)}
                      className="ml-2 text-orange-600 hover:text-orange-800"
                    >
                      ×
                    </button>
                  </span>
                ))}
              </div>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={selectedCuisine}
                  onChange={(e) => setSelectedCuisine(e.target.value)}
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
                  placeholder="Add cuisine..."
                  onKeyPress={(e) => {
                    if (e.key === 'Enter') {
                      e.preventDefault()
                      handleCuisineAdd(selectedCuisine)
                    }
                  }}
                />
                <button
                  type="button"
                  onClick={() => handleCuisineAdd(selectedCuisine)}
                  className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300"
                >
                  Add
                </button>
              </div>
              {meta && (
                <p className="mt-1 text-xs text-gray-500">
                  Popular: {meta.supported_cuisines.slice(0, 8).join(', ')}
                </p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Star className="w-4 h-4 inline mr-1" />
                Minimum Rating: {minimumRating.toFixed(1)}
              </label>
              <input
                type="range"
                min="1"
                max="5"
                step="0.1"
                value={minimumRating}
                onChange={(e) => setMinimumRating(parseFloat(e.target.value))}
                className="w-full"
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-orange-500 text-white py-3 rounded-md hover:bg-orange-600 disabled:bg-gray-400 flex items-center justify-center"
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Finding Recommendations...
                </>
              ) : (
                <>
                  <Search className="w-4 h-4 mr-2" />
                  Get Recommendations
                </>
              )}
            </button>
          </form>

          {error && (
            <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md flex items-start">
              <AlertCircle className="w-4 h-4 text-red-500 mr-2 mt-0.5" />
              <p className="text-red-700 text-sm">{error}</p>
            </div>
          )}
        </div>

        {recommendations.length > 0 && (
          <div className="space-y-4">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Recommended Restaurants</h2>
            {recommendations.map((restaurant, index) => (
              <div key={index} className="bg-white rounded-lg shadow-md p-6">
                <div className="flex justify-between items-start mb-3">
                  <h3 className="text-lg font-semibold text-gray-900">{restaurant.name}</h3>
                  <div className="flex items-center bg-green-100 text-green-800 px-2 py-1 rounded">
                    <Star className="w-4 h-4 mr-1" />
                    {restaurant.rating.toFixed(1)}
                  </div>
                </div>
                
                <div className="flex flex-wrap gap-2 mb-3">
                  {restaurant.cuisines.map((cuisine) => (
                    <span key={cuisine} className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-sm">
                      {cuisine}
                    </span>
                  ))}
                  <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm">
                    {restaurant.estimated_cost}
                  </span>
                </div>
                
                <p className="text-gray-600 text-sm">{restaurant.explanation}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default App
