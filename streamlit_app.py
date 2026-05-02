import streamlit as st

st.title("Zomato AI")
st.write("Restaurant Recommendations")

if st.button("Get Started"):
    st.success("Welcome to Zomato AI!")
    st.write("This is a working Streamlit app.")

st.sidebar.write("Preferences")
location = st.sidebar.text_input("Location")
budget = st.sidebar.selectbox("Budget", ["low", "medium", "high"])

if location:
    st.write(f"Selected location: {location}")
    st.write(f"Selected budget: {budget}")
