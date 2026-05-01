"use client";

import { Search, AlertCircle, RefreshCw } from "lucide-react";

interface EmptyStateProps {
  onNewSearch?: () => void;
}

export function EmptyState({ onNewSearch }: EmptyStateProps) {
  return (
    <div className="text-center py-12">
      <div className="flex justify-center mb-4">
        <div className="p-3 bg-gray-100 rounded-full">
          <Search className="w-8 h-8 text-gray-400" />
        </div>
      </div>
      
      <h3 className="text-lg font-medium text-gray-900 mb-2">No restaurants found</h3>
      
      <p className="text-gray-600 mb-6 max-w-md mx-auto">
        We couldn't find any restaurants that match your preferences. Try adjusting your filters or search criteria.
      </p>
      
      {onNewSearch && (
        <button
          onClick={onNewSearch}
          className="inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition-colors"
        >
          <RefreshCw className="w-4 h-4 mr-2" />
          Try New Search
        </button>
      )}
      
      <div className="mt-8 text-left max-w-md mx-auto">
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-start">
            <AlertCircle className="w-5 h-5 text-blue-500 mr-2 mt-0.5" />
            <div>
              <h4 className="text-sm font-medium text-blue-900 mb-2">Suggestions:</h4>
              <ul className="text-sm text-blue-700 space-y-1">
                <li>• Try a different location or nearby area</li>
                <li>• Adjust your budget range</li>
                <li>• Add more cuisine options</li>
                <li>• Lower the minimum rating requirement</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
