"use client";

import { useState, useEffect } from "react";
import { MapPin, DollarSign, Star, Utensils, Loader2, AlertCircle } from "lucide-react";
import { RecommendationRequest, RestaurantRecommendation, MetaResponse } from "@/types/api";
import { apiService } from "@/services/api";

interface PreferenceFormProps {
  onRecommendations: (recommendations: RestaurantRecommendation[]) => void;
  onLoading: (loading: boolean) => void;
  onError: (error: string) => void;
  isLoading: boolean;
  onLocationChange?: (location: string) => void;
}

export function PreferenceForm({ onRecommendations, onLoading, onError, isLoading, onLocationChange }: PreferenceFormProps) {
  const [formData, setFormData] = useState<RecommendationRequest>({
    location: "",
    budget_band: "medium",
    cuisines: [],
    minimum_rating: 4.0,
    top_k: 5,
    source: "hf",
  });

  const [selectedCuisine, setSelectedCuisine] = useState("");
  const [meta, setMeta] = useState<MetaResponse | null>(null);
  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    loadMetadata();
  }, []);

  const loadMetadata = async () => {
    try {
      const metadata = await apiService.getMetadata();
      setMeta(metadata);
    } catch (error) {
      console.error("Failed to load metadata:", error);
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.location.trim()) {
      newErrors.location = "Location is required";
    }

    if (formData.cuisines.length === 0) {
      newErrors.cuisines = "At least one cuisine is required";
    }

    if (formData.minimum_rating < 1 || formData.minimum_rating > 5) {
      newErrors.minimum_rating = "Rating must be between 1 and 5";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleCuisineAdd = () => {
    if (selectedCuisine.trim() && !formData.cuisines.includes(selectedCuisine.trim())) {
      setFormData({
        ...formData,
        cuisines: [...formData.cuisines, selectedCuisine.trim()],
      });
      setSelectedCuisine("");
      if (errors.cuisines) {
        setErrors({ ...errors, cuisines: "" });
      }
    }
  };

  const handleCuisineRemove = (cuisine: string) => {
    setFormData({
      ...formData,
      cuisines: formData.cuisines.filter((c) => c !== cuisine),
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    onLoading(true);
    onError("");

    try {
      const response = await apiService.getRecommendations(formData);
      onRecommendations(response.recommendations);

      if (response.recommendations.length === 0) {
        if (response.source === "no_candidates") {
          onError("No restaurants found matching your criteria. Try adjusting your filters.");
        } else {
          onError("No recommendations available at the moment. Please try again.");
        }
      }
    } catch (error: any) {
      onError(error.response?.data?.detail || "Failed to get recommendations. Please try again.");
      onRecommendations([]);
    } finally {
      onLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Location Input */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          <MapPin className="w-4 h-4 inline mr-1" />
          Location
        </label>
        <input
          type="text"
          value={formData.location}
          onChange={(e) => {
            setFormData({ ...formData, location: e.target.value });
            if (errors.location) {
              setErrors({ ...errors, location: "" });
            }
            if (onLocationChange) {
              onLocationChange(e.target.value);
            }
          }}
          className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 ${
            errors.location ? "border-red-500" : "border-gray-300"
          }`}
          placeholder="Enter city or area..."
        />
        {errors.location && (
          <p className="mt-1 text-sm text-red-600">{errors.location}</p>
        )}
        {meta && (
          <p className="mt-1 text-xs text-gray-500">
            Available cities: {meta.allowed_cities.slice(0, 5).join(", ")}
            {meta.allowed_cities.length > 5 && "..."}
          </p>
        )}
      </div>

      {/* Budget Selection */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          <DollarSign className="w-4 h-4 inline mr-1" />
          Budget
        </label>
        <div className="flex space-x-4">
          {["low", "medium", "high"].map((budget) => (
            <label key={budget} className="flex items-center">
              <input
                type="radio"
                value={budget}
                checked={formData.budget_band === budget}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    budget_band: e.target.value as "low" | "medium" | "high",
                  })
                }
                className="mr-2"
              />
              <span className="capitalize">{budget}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Cuisine Selection */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          <Utensils className="w-4 h-4 inline mr-1" />
          Cuisines
        </label>
        <div className="flex flex-wrap gap-2 mb-2">
          {formData.cuisines.map((cuisine) => (
            <span
              key={cuisine}
              className="bg-primary-100 text-primary-800 px-3 py-1 rounded-full text-sm flex items-center"
            >
              {cuisine}
              <button
                type="button"
                onClick={() => handleCuisineRemove(cuisine)}
                className="ml-2 text-primary-600 hover:text-primary-800"
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
            className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            placeholder="Add cuisine..."
            onKeyPress={(e) => {
              if (e.key === "Enter") {
                e.preventDefault();
                handleCuisineAdd();
              }
            }}
          />
          <button
            type="button"
            onClick={handleCuisineAdd}
            className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300"
          >
            Add
          </button>
        </div>
        {errors.cuisines && (
          <p className="mt-1 text-sm text-red-600">{errors.cuisines}</p>
        )}
        {meta && (
          <p className="mt-1 text-xs text-gray-500">
            Popular: {meta.supported_cuisines.slice(0, 8).join(", ")}
          </p>
        )}
      </div>

      {/* Rating Slider */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          <Star className="w-4 h-4 inline mr-1" />
          Minimum Rating: {formData.minimum_rating.toFixed(1)}
        </label>
        <input
          type="range"
          min="1"
          max="5"
          step="0.1"
          value={formData.minimum_rating}
          onChange={(e) => {
            setFormData({
              ...formData,
              minimum_rating: parseFloat(e.target.value),
            });
            if (errors.minimum_rating) {
              setErrors({ ...errors, minimum_rating: "" });
            }
          }}
          className="w-full"
        />
        {errors.minimum_rating && (
          <p className="mt-1 text-sm text-red-600">{errors.minimum_rating}</p>
        )}
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={isLoading}
        className="w-full bg-primary-600 text-white py-3 rounded-md hover:bg-primary-700 disabled:bg-gray-400 flex items-center justify-center transition-colors"
      >
        {isLoading ? (
          <>
            <Loader2 className="w-4 h-4 mr-2 animate-spin" />
            Finding Recommendations...
          </>
        ) : (
          "Get Recommendations"
        )}
      </button>
    </form>
  );
}
