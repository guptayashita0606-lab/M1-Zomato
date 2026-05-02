"""
Streamlit application for restaurant recommendations.
Phase 8 - Single-process Python deployment path.
"""

import streamlit as st
import sys
import os
import requests
import json
from typing import List, Dict, Any, Optional
import time

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from .theme import get_theme_config, get_custom_css

# Configure page
st.set_page_config(
    page_title="Zomato AI - Restaurant Recommendations",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply theme configuration
theme_config = get_theme_config()
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Constants
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8004")
CACHE_TTL = 300  # 5 minutes cache

@st.cache_data(ttl=CACHE_TTL)
def load_metadata() -> Dict[str, Any]:
    """Load metadata from backend API with caching."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/meta", timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Failed to load restaurant data: {e}")
        return {
            "allowed_cities": [],
            "supported_budget_bands": ["low", "medium", "high"],
            "supported_cuisines": [],
            "rating_range": {"min": 1.0, "max": 5.0}
        }

@st.cache_data(ttl=CACHE_TTL)
def get_recommendations_cached(location: str, budget_band: str, cuisines: List[str], 
                              minimum_rating: float, top_k: int) -> Dict[str, Any]:
    """Get recommendations with caching."""
    try:
        request_data = {
            "location": location,
            "budget_band": budget_band,
            "cuisines": cuisines,
            "minimum_rating": minimum_rating,
            "top_k": top_k
        }
        
        response = requests.post(
            f"{API_BASE_URL}/api/v1/recommendations", 
            json=request_data, 
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        st.error("Request timed out. Please try again.")
        return {"recommendations": [], "source": "error"}
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the recommendation service. Please check if the backend is running.")
        return {"recommendations": [], "source": "error"}
    except Exception as e:
        st.error(f"Failed to get recommendations: {e}")
        return {"recommendations": [], "source": "error"}

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
    
    # Load metadata
    metadata = load_metadata()
    
    # Location input
    location = st.sidebar.text_input(
        "📍 Location (optional)",
        placeholder="Enter city or area...",
        help="Leave empty to search all locations"
    )
    
    # Budget selection
    budget_band = st.sidebar.selectbox(
        "💰 Budget",
        options=metadata.get("supported_budget_bands", ["low", "medium", "high"]),
        help="Select your preferred budget range"
    )
    
    # Rating slider
    rating_range = metadata.get("rating_range", {"min": 1.0, "max": 5.0})
    minimum_rating = st.sidebar.slider(
        "⭐ Minimum Rating",
        min_value=float(rating_range["min"]),
        max_value=float(rating_range["max"]),
        value=4.0,
        step=0.1,
        help="Minimum restaurant rating"
    )
    
    # Cuisine selection
    available_cuisines = metadata.get("supported_cuisines", [])
    selected_cuisines = st.sidebar.multiselect(
        "🍽️ Cuisines (optional)",
        options=available_cuisines,
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
            recommendations_data = get_recommendations_cached(
                preferences["location"],
                preferences["budget_band"],
                preferences["cuisines"],
                preferences["minimum_rating"],
                preferences["top_k"]
            )
            
            recommendations = recommendations_data.get("recommendations", [])
            source = recommendations_data.get("source", "unknown")
            
            # Store in session state
            st.session_state.recommendations = recommendations
            st.session_state.source = source
            st.session_state.preferences = preferences
    
    # Display recommendations if available
    if "recommendations" in st.session_state:
        recommendations = st.session_state.recommendations
        source = st.session_state.source
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
                    "source": source,
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
    - 🍽️ Real restaurant data
    - ⭐ Rating-based filtering
    - 💰 Budget preferences
    
    Built with ❤️ using Streamlit and Hugging Face data.
    """)

def main():
    """Main application entry point."""
    # Initialize session state
    if "recommendations" not in st.session_state:
        st.session_state.recommendations = None
    if "source" not in st.session_state:
        st.session_state.source = None
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
        f"API: {API_BASE_URL}"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
