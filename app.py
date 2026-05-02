"""
Standalone Streamlit application for restaurant recommendations.
Phase 8 - Complete standalone version for reliable deployment.
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

# Custom CSS for Rosy Hearth theme
st.markdown("""
<style>
/* Rosy Hearth brand colors */
.stButton > button {
    background-color: #b7122a;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-weight: 600;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background-color: #db313f;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(183, 18, 42, 0.3);
}

.stSelectbox > div > div > select {
    border-radius: 8px;
    border: 2px solid #f8e8ea;
    background-color: #ffffff;
}

.stSlider > div > div > div {
    background-color: #b7122a;
}

.stTextInput > div > div > input {
    border-radius: 8px;
    border: 2px solid #f8e8ea;
    background-color: #ffffff;
}

.stTextInput > div > div > input:focus {
    border-color: #b7122a;
    box-shadow: 0 0 0 3px rgba(183, 18, 42, 0.1);
}

/* Restaurant card styling */
.restaurant-card {
    background: white;
    border: 1px solid #f8e8ea;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    transition: all 0.2s ease;
}

.restaurant-card:hover {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    transform: translateY(-2px);
}

.restaurant-name {
    font-family: 'Epilogue', serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: #1c1c1c;
    margin-bottom: 0.5rem;
}

.restaurant-location {
    color: #666666;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
}

.restaurant-cuisines {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin: 0.5rem 0;
}

.cuisine-tag {
    background-color: #f8e8ea;
    color: #b7122a;
    padding: 0.25rem 0.75rem;
    border-radius: 16px;
    font-size: 0.8rem;
    font-weight: 500;
}

.restaurant-rating {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin: 0.5rem 0;
}

.rating-stars {
    color: #b7122a;
    font-weight: 600;
}

.restaurant-explanation {
    color: #666666;
    font-size: 0.9rem;
    line-height: 1.5;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid #f8e8ea;
}

/* Header styling */
.main-header {
    text-align: center;
    margin-bottom: 2rem;
    padding: 2rem 0;
    background: linear-gradient(135deg, #fcf9f8 0%, #f8e8ea 100%);
    border-radius: 12px;
}

.main-title {
    font-family: 'Epilogue', serif;
    font-size: 2.5rem;
    font-weight: 800;
    color: #b7122a;
    margin-bottom: 0.5rem;
}

.main-subtitle {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #666666;
    font-size: 1.1rem;
}

/* Empty state styling */
.empty-state {
    text-align: center;
    padding: 3rem 1rem;
    color: #666666;
}

.empty-state-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    opacity: 0.5;
}

/* Page background */
body {
    background-color: #fcf9f8;
}

.stApp {
    background-color: #fcf9f8;
}
</style>
""", unsafe_allow_html=True)

# Sample restaurant data - no external dependencies
SAMPLE_RESTAURANTS = [
    {
        "name": "Bukhara",
        "location": "Delhi",
        "cuisines": ["North Indian", "Mughlai", "Kebab"],
        "estimated_cost": "high",
        "rating": 4.5,
        "explanation": "Authentic Mughlai cuisine with excellent ambiance and service. Perfect for traditional Indian dining experience."
    },
    {
        "name": "Mainland China",
        "location": "Bangalore",
        "cuisines": ["Chinese", "Asian", "Sichuan"],
        "estimated_cost": "medium",
        "rating": 4.2,
        "explanation": "Authentic Chinese cuisine with modern presentation. Known for excellent dim sum and stir-fry dishes."
    },
    {
        "name": "Saravana Bhavan",
        "location": "Chennai",
        "cuisines": ["South Indian", "Vegetarian", "Dosas"],
        "estimated_cost": "low",
        "rating": 4.0,
        "explanation": "Traditional South Indian vegetarian restaurant. Famous for authentic dosas and filter coffee."
    },
    {
        "name": "Leopold Cafe",
        "location": "Mumbai",
        "cuisines": ["Continental", "Cafe", "Multi-cuisine"],
        "estimated_cost": "medium",
        "rating": 4.3,
        "explanation": "Trendy cafe with colonial ambiance. Great for casual meetings and European cuisine."
    },
    {
        "name": "Dominos Pizza",
        "location": "Mumbai",
        "cuisines": ["Pizza", "Fast Food", "Italian"],
        "estimated_cost": "low",
        "rating": 3.8,
        "explanation": "Popular pizza chain with quick delivery and consistent quality. Great for casual dining."
    },
    {
        "name": "Meghana Foods",
        "location": "Bangalore",
        "cuisines": ["Biryani", "North Indian", "Chinese"],
        "estimated_cost": "medium",
        "rating": 4.4,
        "explanation": "Famous for authentic biryani and North Indian dishes. Always crowded with food lovers."
    },
    {
        "name": "The Coffee Shack",
        "location": "Banashankari",
        "cuisines": ["Cafe", "Chinese", "Continental"],
        "estimated_cost": "medium",
        "rating": 4.2,
        "explanation": "Cozy cafe serving great coffee and multi-cuisine dishes. Perfect for casual dining."
    },
    {
        "name": "Kabab Magic",
        "location": "Basavanagudi",
        "cuisines": ["North Indian", "Kebab", "Chinese"],
        "estimated_cost": "medium",
        "rating": 4.1,
        "explanation": "Specializes in delicious kebabs and North Indian cuisine. Great for meat lovers."
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

def render_restaurant_card(restaurant: Dict[str, Any]) -> None:
    """Render a single restaurant recommendation card."""
    with st.container():
        st.markdown(f"""
        <div class="restaurant-card">
            <div class="restaurant-name">{restaurant.get('name', 'Unknown Restaurant')}</div>
            <div class="restaurant-location">📍 {restaurant.get('location', 'Unknown Location')}</div>
            <div class="restaurant-cuisines">
                {"".join([f'<span class="cuisine-tag">{cuisine}</span>' for cuisine in restaurant.get('cuisines', [])[:5]])}
            </div>
            <div class="restaurant-rating">
                <span class="rating-stars">⭐ {restaurant.get('rating', 0):.1f}</span>
                <span style="color: #666666;">• {restaurant.get('estimated_cost', 'medium').title()} Budget</span>
            </div>
            <div class="restaurant-explanation">
                💡 {restaurant.get('explanation', 'No explanation available.')}
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_empty_state(message: str, show_suggestions: bool = True) -> None:
    """Render empty state with helpful suggestions."""
    st.markdown(f"""
    <div class="empty-state">
        <div class="empty-state-icon">🔍</div>
        <h3>{message}</h3>
        {"<p>Try adjusting your filters:</p><ul><li>Lower the minimum rating</li><li>Try different cuisines</li><li>Search in a different location</li></ul>" if show_suggestions else ""}
    </div>
    """, unsafe_allow_html=True)

def render_sidebar() -> Dict[str, Any]:
    """Render sidebar with preference inputs."""
    st.sidebar.markdown("## 🎯 Your Preferences")
    
    # Get unique cities and cuisines from sample data
    cities = sorted(list(set([r["location"] for r in SAMPLE_RESTAURANTS])))
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
    
    return {
        "location": location.strip(),
        "budget_band": budget_band,
        "cuisines": selected_cuisines,
        "minimum_rating": minimum_rating,
        "top_k": top_k
    }

def render_header() -> None:
    """Render application header."""
    st.markdown("""
    <div class="main-header">
        <div class="main-title">Zomato AI</div>
        <div class="main-subtitle">AI-Powered Restaurant Recommendations</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

def render_main_content(preferences: Dict[str, Any]) -> None:
    """Render main content area with recommendations."""
    
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
                render_restaurant_card(restaurant)
                st.markdown("---")
            
            # Show source info
            with st.expander("📊 Recommendation Details"):
                st.json({
                    "source": "sample_data",
                    "preferences": preferences,
                    "total_found": len(recommendations)
                })
        else:
            render_empty_state(
                "No restaurants found matching your criteria",
                show_suggestions=True
            )

def render_about_section() -> None:
    """Render about section in sidebar."""
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

def main():
    """Main application entry point."""
    # Initialize session state
    if "recommendations" not in st.session_state:
        st.session_state.recommendations = None
    if "preferences" not in st.session_state:
        st.session_state.preferences = None
    
    # Render components
    render_header()
    
    # Create columns for layout
    col1, col2 = st.columns([1, 3])
    
    with col1:
        preferences = render_sidebar()
        render_about_section()
    
    with col2:
        render_main_content(preferences)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666666; padding: 1rem;'>"
        "🍽️ Zomato AI - Phase 8 Streamlit Deployment | "
        "Standalone Version - No External Dependencies"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
