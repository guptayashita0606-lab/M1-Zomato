"use client";

import { RestaurantRecommendation } from "@/types/api";
import { Star, MapPin, DollarSign, Utensils, Copy } from "lucide-react";

interface RestaurantCardProps {
  restaurant: RestaurantRecommendation;
}

export function RestaurantCard({ restaurant }: RestaurantCardProps) {
  const handleCopyAsMarkdown = () => {
    const markdown = `## ${restaurant.name}

**Cuisines:** ${restaurant.cuisines.join(", ")}  
**Rating:** ${restaurant.rating.toFixed(1)} ⭐  
**Cost:** ${restaurant.estimated_cost}  
**Why we recommend it:** ${restaurant.explanation}`;

    navigator.clipboard.writeText(markdown).then(() => {
      // You could add a toast notification here
      console.log("Copied to clipboard!");
    });
  };

  const getBudgetIcon = (cost: string) => {
    if (cost.includes("$") || cost.includes("₹")) {
      const dollarCount = (cost.match(/\$|₹/g) || []).length;
      return (
        <div className="flex items-center">
          {[...Array(Math.min(dollarCount, 3))].map((_, i) => (
            <DollarSign key={i} className="w-4 h-4 text-green-600" />
          ))}
        </div>
      );
    }
    return <span className="text-sm text-gray-600">{cost}</span>;
  };

  return (
    <div className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow p-6">
      <div className="flex justify-between items-start mb-4">
        <div className="flex-1">
          <h3 className="text-xl font-semibold text-gray-900 mb-2">{restaurant.name}</h3>
          <div className="flex items-center space-x-4 text-sm text-gray-600">
            <div className="flex items-center">
              <Star className="w-4 h-4 text-yellow-500 mr-1" />
              <span className="font-medium">{restaurant.rating.toFixed(1)}</span>
            </div>
            {getBudgetIcon(restaurant.estimated_cost)}
          </div>
        </div>
        <button
          onClick={handleCopyAsMarkdown}
          className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-md transition-colors"
          title="Copy as Markdown"
        >
          <Copy className="w-4 h-4" />
        </button>
      </div>

      <div className="mb-4">
        <div className="flex flex-wrap gap-2">
          {restaurant.cuisines.map((cuisine) => (
            <span
              key={cuisine}
              className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800"
            >
              <Utensils className="w-3 h-3 mr-1" />
              {cuisine}
            </span>
          ))}
        </div>
      </div>

      <div className="border-t pt-4">
        <h4 className="text-sm font-medium text-gray-900 mb-2">Why we recommend this</h4>
        <p className="text-sm text-gray-600 leading-relaxed">{restaurant.explanation}</p>
      </div>
    </div>
  );
}
