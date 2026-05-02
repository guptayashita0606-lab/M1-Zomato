import streamlit as st

# Sample restaurant data
restaurants = [
    {"name": "Bukhara", "location": "Delhi", "cuisines": ["North Indian", "Mughlai"], "rating": 4.5, "cost": "high"},
    {"name": "Mainland China", "location": "Bangalore", "cuisines": ["Chinese", "Asian"], "rating": 4.2, "cost": "medium"},
    {"name": "Saravana Bhavan", "location": "Chennai", "cuisines": ["South Indian", "Vegetarian"], "rating": 4.0, "cost": "low"},
    {"name": "Leopold Cafe", "location": "Mumbai", "cuisines": ["Continental", "Cafe"], "rating": 4.3, "cost": "medium"},
    {"name": "Dominos Pizza", "location": "Mumbai", "cuisines": ["Pizza", "Fast Food"], "rating": 3.8, "cost": "low"}
]

def main():
    st.title("🍽️ Zomato AI")
    st.write("AI-Powered Restaurant Recommendations")
    
    # Sidebar
    st.sidebar.header("Preferences")
    location = st.sidebar.text_input("Location (optional)")
    budget = st.sidebar.selectbox("Budget", ["any", "low", "medium", "high"])
    min_rating = st.sidebar.slider("Minimum Rating", 1.0, 5.0, 4.0)
    
    # Filter restaurants
    filtered = []
    for r in restaurants:
        if location and location.lower() not in r["location"].lower():
            continue
        if budget != "any" and r["cost"] != budget:
            continue
        if r["rating"] < min_rating:
            continue
        filtered.append(r)
    
    # Get recommendations button
    if st.button("Get Recommendations"):
        if filtered:
            st.success(f"Found {len(filtered)} restaurants!")
            for i, r in enumerate(filtered, 1):
                st.write(f"**{i}. {r['name']}**")
                st.write(f"📍 {r['location']} | 🍽️ {', '.join(r['cuisines'])} | ⭐ {r['rating']} | 💰 {r['cost']}")
                st.write("---")
        else:
            st.warning("No restaurants found. Try adjusting your filters.")
    
    st.sidebar.info("Built with Streamlit")

if __name__ == "__main__":
    main()
