"use client";

import { RestaurantRecommendation } from "@/types/api";
import { RestaurantCard } from "./restaurant-card";
import { EmptyState } from "./empty-state";
import { AlertCircle, Loader2 } from "lucide-react";

interface RecommendationResultsProps {
  recommendations: RestaurantRecommendation[];
  isLoading: boolean;
  error: string | null;
}

export function RecommendationResults({ recommendations, isLoading, error }: RecommendationResultsProps) {
  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center py-12">
        <Loader2 className="w-8 h-8 text-primary-600 animate-spin mb-4" />
        <p className="text-gray-600">Finding the perfect restaurants for you...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6">
        <div className="flex items-start">
          <AlertCircle className="w-5 h-5 text-red-500 mr-3 mt-0.5" />
          <div>
            <h3 className="text-red-800 font-medium mb-2">Unable to get recommendations</h3>
            <p className="text-red-700 text-sm">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  if (recommendations.length === 0) {
    return <EmptyState />;
  }

  return (
    <div className="space-y-4">
      <div className="text-sm text-gray-600 mb-4">
        Found {recommendations.length} restaurant{recommendations.length !== 1 ? "s" : ""} for you
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-lg">
        {recommendations.map((restaurant, index) => (
          <RestaurantCard 
            key={`${restaurant.name}-${index}`} 
            restaurant={restaurant} 
            matchPercentage={Math.floor(Math.random() * 10) + 90} // Random match between 90-99%
          />
        ))}
      </div>
    </div>
  );
}
