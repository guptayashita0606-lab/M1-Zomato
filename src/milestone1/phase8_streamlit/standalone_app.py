"""
Standalone Streamlit application for restaurant recommendations.
Phase 8 - Standalone deployment without external backend dependency.
"""

import streamlit as st
import sys
import os
import json
import re
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
CACHE_TTL = 300  # 5 minutes cache

# Sample restaurant data for fallback
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
    }
]

def extract_rating(rate_str: str) -> float:
    """Extract numeric rating from string like '3.8/5'"""
    if not rate_str or rate_str == '--':
        return 0.0
    try:
        match = re.search(r'(\d+\.?\d*)', str(rate_str))
        if match:
            return float(match.group(1))
    except:
        pass
    return 0.0

def extract_cost(cost_str: str) -> str:
    """Extract and normalize cost from string"""
    if not cost_str:
        return "medium"
    
    try:
        cost_match = re.search(r'(\d+)', str(cost_str))
        if cost_match:
            cost_num = int(cost_match.group(1))
            if cost_num <= 300:
                return "low"
            elif cost_num <= 700:
                return "medium"
            else:
                return "high"
    except:
        pass
    return "medium"

def normalize_cuisine_list(cuisine_str: str) -> List[str]:
    """Normalize cuisine string to list"""
    if not cuisine_str or cuisine_str == '[]':
        return []
    
    cuisines = [c.strip() for c in str(cuisine_str).split(',')]
    return [c for c in cuisines if c and c != '[]']

@st.cache_data(ttl=CACHE_TTL)
def load_restaurant_data() -> tuple[List[Dict[str, Any]], List[str], List[str]]:
    """Load restaurant data directly from Hugging Face or fallback to sample data."""
    restaurants = []
    cities = []
    cuisines = []
    
    # Try multiple approaches to load Hugging Face data
    hf_load_attempts = [
        {
            "name": "Streaming approach",
            "func": lambda: load_dataset(
                "ManikaSaini/zomato-restaurant-recommendation",
                split="train",
                revision="main",
                streaming=True
            )
        },
        {
            "name": "Standard approach",
            "func": lambda: load_dataset(
                "ManikaSaini/zomato-restaurant-recommendation",
                split="train",
                revision="main"
            )
        },
        {
            "name": "No revision",
            "func": lambda: load_dataset(
                "ManikaSaini/zomato-restaurant-recommendation",
                split="train"
            )
        }
    ]
    
    dataset = None
    loading_method = None
    
    for attempt in hf_load_attempts:
        try:
            with st.spinner(f"Trying {attempt['name']}..."):
                # Check if datasets package is available
                try:
                    from datasets import load_dataset
                except ImportError as e:
                    st.error("❌ datasets package not available. Please install: pip install datasets")
                    break
                
                dataset = attempt["func"]()
                loading_method = attempt["name"]
                st.success(f"✅ Successfully loaded using {attempt['name']}")
                break
                
        except Exception as e:
            st.warning(f"⚠️ {attempt['name']} failed: {str(e)[:100]}...")
            continue
    
    # Process data if successfully loaded
    if dataset is not None:
        try:
            with st.spinner("Processing restaurant data..."):
                processed_restaurants = []
                all_cities = set()
                all_cuisines = set()
                count = 0
                max_items = 100  # Reduced for better performance
                
                if hasattr(dataset, 'select'):
                    # Regular dataset - take first N items
                    limited_data = dataset.select(range(min(max_items, len(dataset))))
                    for row in limited_data:
                        if process_restaurant_row(row, processed_restaurants, all_cities, all_cuisines):
                            count += 1
                else:
                    # Streaming dataset
                    for row in dataset:
                        if count >= max_items:
                            break
                        if process_restaurant_row(row, processed_restaurants, all_cities, all_cuisines):
                            count += 1
                
                restaurants = processed_restaurants
                cities = sorted(list(all_cities))
                cuisines = sorted(list(all_cuisines))[:30]  # Reduced for performance
                
                st.success(f"✅ Loaded {len(restaurants)} restaurants from Hugging Face using {loading_method}")
                
        except Exception as e:
            st.error(f"❌ Error processing Hugging Face data: {e}")
            dataset = None
    
    # Fallback to sample data if Hugging Face failed
    if dataset is None or len(restaurants) == 0:
        st.info("🍽️ Using sample restaurant data for demonstration")
        restaurants = SAMPLE_RESTAURANTS
        cities = list(set([r["location"] for r in restaurants]))
        cuisines = list(set([cuisine for r in restaurants for cuisine in r["cuisines"]]))
        
        st.info(f"✅ Loaded {len(restaurants)} sample restaurants")
    
    return restaurants, cities, cuisines

def process_restaurant_row(row, processed_restaurants, all_cities, all_cuisines) -> bool:
    """Process a single restaurant row from the dataset."""
    try:
        name = row.get('name', '').strip()
        location = row.get('location', '').strip()
        rate = row.get('rate', '')
        cost = row.get('approx_cost(for two people)', '')
        cuisine_str = row.get('cuisines', '')
        
        if not name or not location:
            return False
        
        rating = extract_rating(rate)
        cost_band = extract_cost(cost)
        cuisine_list = normalize_cuisine_list(cuisine_str)
        
        if rating < 2.0:
            return False
        
        restaurant = {
            "name": name,
            "location": location,
            "cuisines": cuisine_list,
            "estimated_cost": cost_band,
            "rating": rating,
            "explanation": f"Popular {', '.join(cuisine_list[:2])} restaurant in {location} with {rating} rating."
        }
        
        processed_restaurants.append(restaurant)
        all_cities.add(location)
        for cuisine in cuisine_list:
            if cuisine and len(cuisine) > 2:
                all_cuisines.add(cuisine)
        
        return True
        
    except Exception:
        return False

def get_recommendations(restaurants: List[Dict[str, Any]], location: str, budget_band: str, 
                       cuisines: List[str], minimum_rating: float, top_k: int) -> List[Dict[str, Any]]:
    """Get recommendations based on filters."""
    filtered = []
    
    for restaurant in restaurants:
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
    
    # Load data
    restaurants, cities, available_cuisines = load_restaurant_data()
    
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
        "restaurants": restaurants,
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
    restaurants = preferences["restaurants"]
    
    # Get recommendations button
    if st.button("🚀 Get Recommendations", type="primary", use_container_width=True):
        with st.spinner("🤖 Finding the perfect restaurants for you..."):
            recommendations = get_recommendations(
                restaurants,
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
                    "source": "standalone",
                    "preferences": {
                        k: v for k, v in preferences.items() if k != "restaurants"
                    },
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
        "Standalone Version"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
