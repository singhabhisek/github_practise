# app.py

import streamlit as st
import pandas as pd
import requests

# --- Session State Initialization ---
# This is crucial for maintaining state across pages.
# 'page' tracks the current page, 'selected_product_id' stores the product ID.
if 'page' not in st.session_state:
    st.session_state.page = 'search'
if 'selected_product_id' not in st.session_state:
    st.session_state.selected_product_id = None
if 'search_results' not in st.session_state:
    st.session_state.search_results = pd.DataFrame()

# --- Page Functions ---
def search_page():
    """Displays the product search interface and results."""
    st.title("Product Search 🔍")
    st.markdown("Search for products by category and keywords.")

    with st.container(border=True):
        st.subheader("Search Criteria")
        col1, col2, col3 = st.columns([1, 2, 1])

        with col1:
            # We'll use the API to get categories for a real app, but for now we'll hardcode
            categories = ["All", "Electronics", "Accessories"]
            category = st.selectbox("Filter by Category", categories)
        
        with col2:
            search_term = st.text_input("Search by Name or Description", "")
        
        with col3:
            st.write("") # Spacer
            if st.button("Search", use_container_width=True):
                # The actual POST call to the local Flask API
                url = "http://127.0.0.1:5000/search"
                payload = {"category": category, "search_term": search_term}
                headers = {"Authorization": "Bearer my_secret_token"}
                
                try:
                    with st.spinner('Searching...'):
                        response = requests.post(url, json=payload, headers=headers)
                        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
                        results_df = pd.DataFrame(response.json())
                        st.session_state.search_results = results_df
                except requests.exceptions.RequestException as e:
                    st.error(f"Error fetching results from Flask API: {e}")
                    st.session_state.search_results = pd.DataFrame() # Clear results on error
                
    st.write("---")
    
    # Display search results from session state
    if not st.session_state.search_results.empty:
        st.subheader("Search Results")
        
        results_container = st.container(border=True)
        with results_container:
            for index, row in st.session_state.search_results.iterrows():
                col_id, col_name, col_rate, col_action = st.columns([1, 2, 1, 1])
                with col_id:
                    st.markdown(f"**{row['product_id']}**")
                with col_name:
                    st.markdown(f"**{row['name']}**")
                with col_rate:
                    st.markdown(f"${row['rate']:.2f}")
                with col_action:
                    if st.button("View Details", key=f"view_button_{row['product_id']}", use_container_width=True):
                        st.session_state.selected_product_id = row['product_id']
                        st.session_state.page = 'details'
                        st.rerun()
    else:
        # Check if the search button has been clicked and returned no results.
        if st.session_state.search_results is not None and 'search_results' in st.session_state and len(st.session_state.search_results.index) == 0:
            st.info("No products found matching your criteria.")


def product_details_page():
    """Displays the detailed information for a single product."""
    st.subheader("Product Details")
    
    if st.session_state.selected_product_id is not None:
        # The actual GET call to the local Flask API
        product_id = st.session_state.selected_product_id
        url = f"http://127.0.0.1:5000/products/{product_id}"

        try:
            with st.spinner(f"Fetching details for ID {product_id}..."):
                response = requests.get(url)
                response.raise_for_status()
                product_details = response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching product details from Flask API: {e}")
            product_details = None

        if product_details:
            st.title(f"Details for {product_details['name']}")
            st.markdown("---")
            st.container(border=True).markdown(f"""
            - **Product ID:** `{product_details['product_id']}`
            - **Category:** `{product_details['category']}`
            - **Price:** `{product_details['rate']:.2f}`
            - **Description:** {product_details['description']}
            """)

            st.write("") # Spacer
            if st.button("← Back to Search"):
                st.session_state.selected_product_id = None
                st.session_state.page = 'search'
                st.rerun()
    else:
        st.session_state.page = 'search'
        st.rerun()


# --- Main Application Logic ---
if st.session_state.page == 'search':
    search_page()
elif st.session_state.page == 'details':
    product_details_page()
