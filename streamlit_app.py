#!/usr/bin/env python3
"""
Streamlit app entry point for deployment.
This file serves as the main entry point for Streamlit Community Cloud deployment.
"""

import streamlit as st
from typing import List, Dict, Any

# Configure page
st.set_page_config(
    page_title="Zomato AI - Restaurant Recommendations",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sample restaurant data
SAMPLE_RESTAURANTS = [
    {
        "name": "Bukhara",
        "location": "Delhi",
        "cuisines": ["North Indian", "Mughlai", "Kebab"],
        "estimated_cost": "high",
        "rating": 4.5,
        "explanation": "Authentic Mughlai cuisine with excellent ambiance and service."
    },
    {
        "name": "Mainland China",
        "location": "Bangalore",
        "cuisines": ["Chinese", "Asian", "Sichuan"],
        "estimated_cost": "medium",
        "rating": 4.2,
        "explanation": "Authentic Chinese cuisine with modern presentation."
    },
    {
        "name": "Saravana Bhavan",
        "location": "Chennai",
        "cuisines": ["South Indian", "Vegetarian", "Dosas"],
        "estimated_cost": "low",
        "rating": 4.0,
        "explanation": "Traditional South Indian vegetarian restaurant."
    },
    {
        "name": "Leopold Cafe",
        "location": "Mumbai",
        "cuisines": ["Continental", "Cafe", "Multi-cuisine"],
        "estimated_cost": "medium",
        "rating": 4.3,
        "explanation": "Trendy cafe with colonial ambiance."
    },
    {
        "name": "Dominos Pizza",
        "location": "Mumbai",
        "cuisines": ["Pizza", "Fast Food", "Italian"],
        "estimated_cost": "low",
        "rating": 3.8,
        "explanation": "Popular pizza chain with quick delivery."
    },
    {
        "name": "Meghana Foods",
        "location": "Bangalore",
        "cuisines": ["Biryani", "North Indian", "Chinese"],
        "estimated_cost": "medium",
        "rating": 4.4,
        "explanation": "Famous for authentic biryani and North Indian dishes."
    },
    {
        "name": "The Coffee Shack",
        "location": "Banashankari",
        "cuisines": ["Cafe", "Chinese", "Continental"],
        "estimated_cost": "medium",
        "rating": 4.2,
        "explanation": "Cozy cafe serving great coffee and multi-cuisine dishes."
    },
    {
        "name": "Kabab Magic",
        "location": "Basavanagudi",
        "cuisines": ["North Indian", "Kebab", "Chinese"],
        "estimated_cost": "medium",
        "rating": 4.1,
        "explanation": "Specializes in delicious kebabs and North Indian cuisine."
    }
]

def get_recommendations(location: str, budget_band: str, cuisines: List[str], 
                       minimum_rating: float, top_k: int) -> List[Dict[str, Any]]:
    """Get recommendations based on filters."""
    filtered = []
    
    for restaurant in SAMPLE_RESTAURANTS:
        location_match = not location or location.lower() in restaurant["location"].lower()
        rating_match = restaurant["rating"] >= minimum_rating
        budget_match = budget_band == "any" or restaurant["estimated_cost"] == budget_band
        cuisine_match = not cuisines or any(
            cuisine.lower() in [c.lower() for c in restaurant["cuisines"]] 
            for cuisine in cuisines
        )
        
        if location_match and rating_match and budget_match and cuisine_match:
            filtered.append(restaurant)
    
    # Sort by rating and return top recommendations
    filtered.sort(key=lambda x: x["rating"], reverse=True)
    return filtered[:top_k]

def main():
    """Main application entry point."""
    # Initialize session state
    if "recommendations" not in st.session_state:
        st.session_state.recommendations = None
    if "preferences" not in st.session_state:
        st.session_state.preferences = None
    
    # Header
    st.title("🍽️ Zomato AI")
    st.markdown("AI-Powered Restaurant Recommendations")
    st.markdown("---")
    
    # Sidebar
    st.sidebar.markdown("## 🎯 Your Preferences")
    
    # Get unique cities and cuisines from sample data
    all_cuisines = sorted(list(set([cuisine for r in SAMPLE_RESTAURANTS for cuisine in r["cuisines"]])))
    
    # Location input
    location = st.sidebar.text_input(
        "📍 Location (optional)",
        placeholder="Enter city or area...",
        help="Leave empty to search all locations"
    )
    
    # Budget selection
    budget_band = st.sidebar.selectbox(
        "💰 Budget",
        options=["any", "low", "medium", "high"],
        help="Select your preferred budget range"
    )
    
    # Rating slider
    minimum_rating = st.sidebar.slider(
        "⭐ Minimum Rating",
        min_value=1.0,
        max_value=5.0,
        value=4.0,
        step=0.1,
        help="Minimum restaurant rating"
    )
    
    # Cuisine selection
    selected_cuisines = st.sidebar.multiselect(
        "🍽️ Cuisines (optional)",
        options=all_cuisines,
        help="Select preferred cuisines. Leave empty to search all cuisines."
    )
    
    # Number of recommendations
    top_k = st.sidebar.slider(
        "📊 Number of Recommendations",
        min_value=1,
        max_value=10,
        value=5,
        help="How many recommendations to show"
    )
    
    preferences = {
        "location": location.strip(),
        "budget_band": budget_band,
        "cuisines": selected_cuisines,
        "minimum_rating": minimum_rating,
        "top_k": top_k
    }
    
    # Get recommendations button
    if st.button("🚀 Get Recommendations", type="primary", use_container_width=True):
        with st.spinner("🤖 Finding the perfect restaurants for you..."):
            recommendations = get_recommendations(
                preferences["location"],
                preferences["budget_band"],
                preferences["cuisines"],
                preferences["minimum_rating"],
                preferences["top_k"]
            )
            
            # Store in session state
            st.session_state.recommendations = recommendations
            st.session_state.preferences = preferences
    
    # Display recommendations if available
    if "recommendations" in st.session_state:
        recommendations = st.session_state.recommendations
        preferences = st.session_state.preferences
        
        if recommendations:
            st.success(f"🎉 Found {len(recommendations)} restaurants for you!")
            
            # Render each recommendation
            for i, restaurant in enumerate(recommendations, 1):
                st.markdown(f"### Recommendation {i}")
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{restaurant['name']}**")
                    st.markdown(f"📍 {restaurant['location']}")
                    st.markdown(f"🍽️ {', '.join(restaurant['cuisines'])}")
                    st.markdown(f"⭐ {restaurant['rating']} • {restaurant['estimated_cost'].title()} Budget")
                    st.markdown(f"💡 {restaurant['explanation']}")
                
                with col2:
                    st.markdown(f"# {restaurant['rating']}")
                
                st.markdown("---")
            
            # Show source info
            with st.expander("📊 Recommendation Details"):
                st.json({
                    "source": "sample_data",
                    "preferences": preferences,
                    "total_found": len(recommendations)
                })
        else:
            st.warning("No restaurants found matching your criteria. Try adjusting your filters.")
    
    # About section
    st.sidebar.markdown("---")
    st.sidebar.markdown("## ℹ️ About")
    st.sidebar.info("""
    **Zomato AI** provides personalized restaurant recommendations using:
    
    - 🤖 AI-powered matching
    - 🍽️ Sample restaurant data
    - ⭐ Rating-based filtering
    - 💰 Budget preferences
    
    Built with ❤️ using Streamlit.
    """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666666; padding: 1rem;'>"
        "🍽️ Zomato AI - Phase 8 Streamlit Deployment | "
        "Simplified Version - No External Dependencies"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
