export interface RecommendationRequest {
  location: string;
  budget_band: "low" | "medium" | "high";
  cuisines: string[];
  minimum_rating: number;
  top_k?: number;
  source?: "local" | "hf";
  local_path?: string;
}

export interface RestaurantRecommendation {
  name: string;
  cuisines: string[];
  rating: number;
  estimated_cost: string;
  explanation: string;
  restaurant_id?: string;
}

export interface RecommendationResponse {
  recommendations: RestaurantRecommendation[];
  source: "llm" | "fallback" | "no_candidates";
  total_candidates: number;
  filtered_candidates: number;
  request_id?: string;
  telemetry?: any;
}

export interface MetaResponse {
  allowed_cities: string[];
  supported_budget_bands: string[];
  supported_cuisines: string[];
  rating_range: {
    min: number;
    max: number;
  };
}

export interface HealthResponse {
  status: string;
  version: string;
  dependencies: Record<string, boolean>;
}
