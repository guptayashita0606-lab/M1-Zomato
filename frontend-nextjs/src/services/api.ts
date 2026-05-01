import axios from "axios";
import { RecommendationRequest, RecommendationResponse, MetaResponse, HealthResponse } from "@/types/api";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 35000, // 35 seconds (slightly more than backend timeout)
  headers: {
    "Content-Type": "application/json",
  },
});

export const apiService = {
  async getRecommendations(request: RecommendationRequest): Promise<RecommendationResponse> {
    try {
      const response = await apiClient.post<RecommendationResponse>("/api/v1/recommendations", request);
      return response.data;
    } catch (error: any) {
      console.error("API Error:", error);
      throw error;
    }
  },

  async getMetadata(): Promise<MetaResponse> {
    try {
      const response = await apiClient.get<MetaResponse>("/api/v1/meta");
      return response.data;
    } catch (error: any) {
      console.error("Metadata API Error:", error);
      throw error;
    }
  },

  async getHealth(): Promise<HealthResponse> {
    try {
      const response = await apiClient.get<HealthResponse>("/health");
      return response.data;
    } catch (error: any) {
      console.error("Health API Error:", error);
      throw error;
    }
  },
};
