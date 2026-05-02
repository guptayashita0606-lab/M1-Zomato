"""
Streamlit theme configuration for brand consistency.
Uses Rosy Hearth colors from Phase 7 design system.
"""

def get_theme_config():
    """Get Streamlit theme configuration matching Phase 7 design."""
    return {
        "theme": {
            "primaryColor": "#b7122a",  # Rosy Hearth primary
            "backgroundColor": "#fcf9f8",  # Light background
            "secondaryBackgroundColor": "#ffffff",  # White for cards
            "textColor": "#1c1c1c",  # Dark text
            "font": {
                "sans": ["Plus Jakarta Sans", "sans-serif"],
                "serif": ["Epilogue", "serif"],
                "mono": ["JetBrains Mono", "monospace"]
            }
        }
    }

def get_custom_css():
    """Get custom CSS for enhanced styling."""
    return """
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
    
    /* Loading and error states */
    .loading-container {
        text-align: center;
        padding: 2rem;
        color: #666666;
    }
    
    .error-container {
        background-color: #fef2f2;
        border: 1px solid #fecaca;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: #dc2626;
    }
    
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
    </style>
    """
