#!/usr/bin/env python3
"""
Standalone Streamlit app for deployment.
No external imports - completely self-contained.
"""

import streamlit as st

# Configure page
st.set_page_config(
    page_title="Zomato AI - Restaurant Recommendations",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sample restaurant data
RESTAURANTS = [
    {
        "name": "Bukhara",
        "location": "Delhi", 
        "cuisines": ["North Indian", "Mughlai", "Kebab"],
        "cost": "high",
        "rating": 4.5,
        "explanation": "Authentic Mughlai cuisine with excellent ambiance and service."
    },
    {
        "name": "Mainland China",
        "location": "Bangalore",
        "cuisines": ["Chinese", "Asian", "Sichuan"], 
        "cost": "medium",
        "rating": 4.2,
        "explanation": "Authentic Chinese cuisine with modern presentation."
    },
    {
        "name": "Saravana Bhavan",
        "location": "Chennai",
        "cuisines": ["South Indian", "Vegetarian", "Dosas"],
        "cost": "low", 
        "rating": 4.0,
        "explanation": "Traditional South Indian vegetarian restaurant."
    },
    {
        "name": "Leopold Cafe",
        "location": "Mumbai",
        "cuisines": ["Continental", "Cafe", "Multi-cuisine"],
        "cost": "medium",
        "rating": 4.3,
        "explanation": "Trendy cafe with colonial ambiance."
    },
    {
        "name": "Dominos Pizza", 
        "location": "Mumbai",
        "cuisines": ["Pizza", "Fast Food", "Italian"],
        "cost": "low",
        "rating": 3.8,
        "explanation": "Popular pizza chain with quick delivery."
    },
    {
        "name": "Meghana Foods",
        "location": "Bangalore", 
        "cuisines": ["Biryani", "North Indian", "Chinese"],
        "cost": "medium",
        "rating": 4.4,
        "explanation": "Famous for authentic biryani and North Indian dishes."
    },
    {
        "name": "The Coffee Shack",
        "location": "Banashankari",
        "cuisines": ["Cafe", "Chinese", "Continental"],
        "cost": "medium", 
        "rating": 4.2,
        "explanation": "Cozy cafe serving great coffee and multi-cuisine dishes."
    },
    {
        "name": "Kabab Magic",
        "location": "Basavanagudi",
        "cuisines": ["North Indian", "Kebab", "Chinese"],
        "cost": "medium",
        "rating": 4.1,
        "explanation": "Specializes in delicious kebabs and North Indian cuisine."
    }
]

def filter_restaurants(location, budget, cuisines, min_rating):
    """Filter restaurants based on criteria."""
    filtered = []
    for r in RESTAURANTS:
        location_match = not location or location.lower() in r["location"].lower()
        rating_match = r["rating"] >= min_rating
        budget_match = budget == "any" or r["cost"] == budget
        cuisine_match = not cuisines or any(
            cuisine.lower() in [c.lower() for c in r["cuisines"]] 
            for cuisine in cuisines
        )
        
        if location_match and rating_match and budget_match and cuisine_match:
            filtered.append(r)
    
    return sorted(filtered, key=lambda x: x["rating"], reverse=True)

def main():
    """Main application."""
    # Header
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #fcf9f8 0%, #f8e8ea 100%); border-radius: 12px; margin-bottom: 2rem;'>
        <h1 style='color: #b7122a; font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem;'>🍽️ Zomato AI</h1>
        <p style='color: #666666; font-size: 1.1rem;'>AI-Powered Restaurant Recommendations</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Sidebar
    st.sidebar.markdown("## 🎯 Your Preferences")
    
    # Get all cuisines
    all_cuisines = sorted(list(set([cuisine for r in RESTAURANTS for cuisine in r["cuisines"]])))
    
    # Input controls
    location = st.sidebar.text_input(
        "📍 Location (optional)",
        placeholder="Enter city or area...",
        help="Leave empty to search all locations"
    )
    
    budget = st.sidebar.selectbox(
        "💰 Budget",
        options=["any", "low", "medium", "high"],
        help="Select your preferred budget range"
    )
    
    min_rating = st.sidebar.slider(
        "⭐ Minimum Rating",
        min_value=1.0,
        max_value=5.0,
        value=4.0,
        step=0.1,
        help="Minimum restaurant rating"
    )
    
    selected_cuisines = st.sidebar.multiselect(
        "🍽️ Cuisines (optional)",
        options=all_cuisines,
        help="Select preferred cuisines"
    )
    
    top_k = st.sidebar.slider(
        "📊 Number of Recommendations",
        min_value=1,
        max_value=10,
        value=5,
        help="How many recommendations to show"
    )
    
    # Get recommendations button
    if st.button("🚀 Get Recommendations", type="primary", use_container_width=True):
        with st.spinner("🤖 Finding the perfect restaurants for you..."):
            recommendations = filter_restaurants(
                location.strip(),
                budget,
                selected_cuisines,
                min_rating
            )[:top_k]
            
            if recommendations:
                st.success(f"🎉 Found {len(recommendations)} restaurants for you!")
                
                # Display recommendations
                for i, restaurant in enumerate(recommendations, 1):
                    st.markdown(f"### Recommendation {i}")
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{restaurant['name']}**")
                        st.markdown(f"📍 {restaurant['location']}")
                        st.markdown(f"🍽️ {', '.join(restaurant['cuisines'])}")
                        st.markdown(f"⭐ {restaurant['rating']} • {restaurant['cost'].title()} Budget")
                        st.markdown(f"💡 {restaurant['explanation']}")
                    
                    with col2:
                        st.markdown(f"# {restaurant['rating']}")
                    
                    st.markdown("---")
                
                # Details
                with st.expander("📊 Recommendation Details"):
                    st.json({
                        "source": "sample_data",
                        "preferences": {
                            "location": location.strip(),
                            "budget": budget,
                            "cuisines": selected_cuisines,
                            "minimum_rating": min_rating,
                            "top_k": top_k
                        },
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
        "🍽️ Zomato AI - Standalone Version | No External Dependencies"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
