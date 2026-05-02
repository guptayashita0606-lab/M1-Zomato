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

    // Make location optional - allow empty location to search all cities
    // if (!formData.location.trim()) {
    //   newErrors.location = "Location is required";
    // }

    // Make cuisines optional - allow empty cuisines to search all cuisines
    // if (formData.cuisines.length === 0) {
    //   newErrors.cuisines = "At least one cuisine is required";
    // }

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
      <div className="bg-surface-container-low rounded-lg p-md">
        <label className="block text-sm font-medium text-on-surface mb-sm">
          <span className="material-symbols-outlined text-primary text-[18px] align-middle mr-2">location_on</span>
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
          className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 bg-surface-container-lowest ${
            errors.location ? "border-red-500" : "border-outline"
          }`}
          placeholder="Enter city or area (optional - leave empty to search all cities)"
        />
        {errors.location && (
          <p className="mt-1 text-sm text-error">{errors.location}</p>
        )}
        {meta && (
          <p className="mt-1 text-xs text-on-secondary-container">
            Popular: {meta.allowed_cities.slice(0, 5).join(", ")}
          </p>
        )}
      </div>

      {/* Budget Selection */}
      <div className="bg-surface-container-low rounded-lg p-md">
        <label className="block text-sm font-medium text-on-surface mb-sm">
          <span className="material-symbols-outlined text-primary text-[18px] align-middle mr-2">attach_money</span>
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
              <span className="capitalize text-on-surface">{budget}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Cuisine Selection */}
      <div className="bg-surface-container-low rounded-lg p-md">
        <label className="block text-sm font-medium text-on-surface mb-sm">
          <span className="material-symbols-outlined text-primary text-[18px] align-middle mr-2">restaurant</span>
          Cuisines
        </label>
        <div className="flex flex-wrap gap-2 mb-2">
          {formData.cuisines.map((cuisine) => (
            <span
              key={cuisine}
              className="bg-primary/10 text-primary px-3 py-1 rounded-full text-sm flex items-center border border-primary/20"
            >
              {cuisine}
              <button
                type="button"
                onClick={() => handleCuisineRemove(cuisine)}
                className="ml-2 text-primary hover:text-primary-container"
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
            className="flex-1 px-3 py-2 border border-outline rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 bg-surface-container-lowest"
            placeholder="Add cuisine (optional - leave empty to search all cuisines)"
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
            className="btn-secondary px-4 py-2"
          >
            Add
          </button>
        </div>
        {errors.cuisines && (
          <p className="mt-1 text-sm text-error">{errors.cuisines}</p>
        )}
        {meta && (
          <p className="mt-1 text-xs text-on-secondary-container">
            Popular: {meta.supported_cuisines.slice(0, 8).join(", ")}
          </p>
        )}
      </div>

      {/* Rating Slider */}
      <div className="bg-surface-container-low rounded-lg p-md">
        <label className="block text-sm font-medium text-on-surface mb-sm">
          <span className="material-symbols-outlined text-primary text-[18px] align-middle mr-2">star</span>
          Minimum Rating
        </label>
        <div className="space-y-sm">
          <div className="flex justify-between text-xs text-on-secondary-container">
            <span>1.0</span>
            <span className="font-headline-sm text-primary font-bold">{formData.minimum_rating.toFixed(1)}</span>
            <span>5.0</span>
          </div>
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
            className="w-full h-2 bg-surface-container rounded-lg appearance-none cursor-pointer slider-primary"
            style={{
              background: `linear-gradient(to right, #b7122a 0%, #b7122a ${((formData.minimum_rating - 1) / 4) * 100}%, #e4e2e1 ${((formData.minimum_rating - 1) / 4) * 100}%, #e4e2e1 100%)`
            }}
          />
          <div className="flex justify-between text-xs text-on-secondary-container">
            <span className="text-xs">Any rating</span>
            <span className="text-xs">High quality</span>
          </div>
        </div>
        {errors.minimum_rating && (
          <p className="mt-2 text-sm text-error">{errors.minimum_rating}</p>
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
