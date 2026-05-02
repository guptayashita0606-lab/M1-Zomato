"use client";

import { useState } from "react";
import { PreferenceForm } from "@/components/forms/preference-form";
import { RecommendationResults } from "@/components/recommendations/recommendation-results";
import { Header } from "@/components/layout/header";
import { Sidebar } from "@/components/layout/sidebar";
import { RestaurantRecommendation } from "@/types/api";

export default function Home() {
  const [recommendations, setRecommendations] = useState<RestaurantRecommendation[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searchCompleted, setSearchCompleted] = useState(false);
  const [currentLocation, setCurrentLocation] = useState("Manhattan, NY");

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
    <div className="flex h-screen">
      <Sidebar currentPage="recommendations" />
      
      <main className="flex-1 ml-72 p-8 bg-[#fcf9f8] overflow-auto">
        <Header location={currentLocation} />
        
        {!searchCompleted ? (
          <div className="bg-white rounded-lg shadow-lg border border-red-50 p-8 max-w-4xl mx-auto">
            <div className="text-center mb-8">
              <h2 className="text-4xl font-bold text-[#b7122a] mb-4" style={{ fontFamily: 'Epilogue, sans-serif' }}>
                Find Your Perfect Dining Experience
              </h2>
              <p className="text-lg text-gray-600 max-w-2xl mx-auto" style={{ fontFamily: 'Plus Jakarta Sans, sans-serif' }}>
                Let our AI curate personalized restaurant recommendations based on your unique taste preferences and dining history.
              </p>
            </div>
            
            <PreferenceForm
              onRecommendations={handleRecommendations}
              onLoading={handleLoading}
              onError={handleError}
              isLoading={isLoading}
              onLocationChange={setCurrentLocation}
            />
          </div>
        ) : (
          <div className="space-y-xl">
            <div className="flex justify-between items-center">
              <div>
                <h2 className="text-headline-lg font-headline text-on-surface mb-sm">
                  Your Curated Recommendations
                </h2>
                <p className="text-body-md text-on-secondary-container">
                  Found {recommendations.length} restaurant{recommendations.length !== 1 ? "s" : ""} perfectly matched to your preferences
                </p>
              </div>
              <button
                onClick={handleNewSearch}
                className="btn-secondary"
              >
                <span className="material-symbols-outlined text-sm mr-2">refresh</span>
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
    </div>
  );
}
