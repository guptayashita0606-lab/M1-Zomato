"use client";

import { RestaurantRecommendation } from "@/types/api";

interface RestaurantCardProps {
  restaurant: RestaurantRecommendation;
  matchPercentage?: number;
}

export function RestaurantCard({ restaurant, matchPercentage = 95 }: RestaurantCardProps) {
  const handleCopyAsMarkdown = () => {
    const markdown = `## ${restaurant.name}

**Cuisines:** ${restaurant.cuisines.join(", ")}  
**Rating:** ${restaurant.rating.toFixed(1)} ⭐  
**Cost:** ${restaurant.estimated_cost}  
**Why we recommend it:** ${restaurant.explanation}`;

    navigator.clipboard.writeText(markdown).then(() => {
      console.log("Copied to clipboard!");
    });
  };

  // Generate a placeholder image URL
  const imageUrl = `https://picsum.photos/seed/${restaurant.name.replace(/\s+/g, '-')}/400/300.jpg`;

  return (
    <div className="card group">
      <div className="relative aspect-[1.37] overflow-hidden">
        <img
          alt={restaurant.name}
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
          src={imageUrl}
        />
        <div className="absolute top-md right-md bg-primary px-3 py-1 rounded-full shadow-lg">
          <span className="text-white font-label-sm">{matchPercentage}% Match</span>
        </div>
      </div>
      
      <div className="p-lg">
        <div className="flex justify-between items-start mb-sm">
          <h3 className="font-headline-lg text-xl">{restaurant.name}</h3>
          <div className="flex items-center gap-xs">
            <span className="material-symbols-outlined text-yellow-500 text-sm">star</span>
            <span className="font-bold">{restaurant.rating.toFixed(1)}</span>
          </div>
        </div>
        
        <p className="text-on-secondary-container font-body-md mb-md">
          {restaurant.cuisines.join(" • ")} • {restaurant.estimated_cost} • 1.2 miles
        </p>
        
        <div className="ai-insight mb-md">
          <div className="flex items-center gap-xs text-primary mb-xs">
            <span className="material-symbols-outlined text-[16px]">auto_awesome</span>
            <span className="font-label-sm">AI INSIGHT</span>
          </div>
          <p className="text-on-surface-variant text-sm font-body-md">{restaurant.explanation}</p>
        </div>
        
        <button className="btn-primary w-full">
          Reserve a Table
        </button>
      </div>
    </div>
  );
}
