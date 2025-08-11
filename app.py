# app.py

import streamlit as st

# --- Page functions ---
def home_page():
    """Defines the content for the Home page."""
    st.title("Welcome to My Website! 👋")
    st.markdown("""
        This is the home page of your new Streamlit app.
        You can add text, images, charts, and interactive widgets here.
    """)
    st.write("---")

    # Example interactive widget
    slider_value = st.slider("Select a value", 0, 100, 50)
    st.write(f"The current value is: {slider_value}")

def about_page():
    """Defines the content for the About page."""
    st.title("About This App 🧐")
    st.markdown("""
        This application was built using **Streamlit**, a powerful
        Python library that makes it incredibly easy to create
        data-driven web apps.

        **Key Features:**
        - No HTML/CSS/JavaScript required.
        - Rapid development and deployment.
        - Connects easily with Python libraries like Pandas, Matplotlib, etc.
    """)

# --- Main App Logic ---
st.sidebar.title("Navigation")
# Create a selectbox in the sidebar to switch between pages
page = st.sidebar.radio("Go to", ["Home", "About"])

# Display the selected page content
if page == "Home":
    home_page()
elif page == "About":
    about_page()

st.sidebar.write("---")
st.sidebar.info("This is a simple demo app.")

