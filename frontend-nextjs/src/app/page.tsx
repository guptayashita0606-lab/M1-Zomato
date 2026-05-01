"use client";

import { useState } from "react";
import { PreferenceForm } from "@/components/forms/preference-form";
import { RecommendationResults } from "@/components/recommendations/recommendation-results";
import { Header } from "@/components/layout/header";
import { Footer } from "@/components/layout/footer";
import { RestaurantRecommendation } from "@/types/api";

export default function Home() {
  const [recommendations, setRecommendations] = useState<RestaurantRecommendation[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searchCompleted, setSearchCompleted] = useState(false);

  const handleRecommendations = (results: RestaurantRecommendation[]) => {
    setRecommendations(results);
    setSearchCompleted(true);
  };

  const handleLoading = (loading: boolean) => {
    setIsLoading(loading);
  };

  const handleError = (errorMessage: string) => {
    setError(errorMessage);
  };

  const handleNewSearch = () => {
    setRecommendations([]);
    setError(null);
    setSearchCompleted(false);
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      
      <main className="flex-1 container mx-auto px-4 py-8 max-w-4xl">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Restaurant Recommendations
          </h1>
          <p className="text-lg text-gray-600">
            Discover amazing dining spots tailored to your preferences
          </p>
        </div>

        {!searchCompleted ? (
          <div className="bg-white rounded-lg shadow-md p-6">
            <PreferenceForm
              onRecommendations={handleRecommendations}
              onLoading={handleLoading}
              onError={handleError}
              isLoading={isLoading}
            />
          </div>
        ) : (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-semibold text-gray-900">
                Recommended Restaurants
              </h2>
              <button
                onClick={handleNewSearch}
                className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition-colors"
              >
                New Search
              </button>
            </div>
            
            <RecommendationResults
              recommendations={recommendations}
              isLoading={isLoading}
              error={error}
            />
          </div>
        )}
      </main>

      <Footer />
    </div>
  );
}
