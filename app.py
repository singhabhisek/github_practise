# app.py

import streamlit as st
import pandas as pd
import time # For simulating a loading screen

# --- Sample Data ---
# In a real application, this data would come from a database or an API.
products = {
    "product_id": [101, 102, 103, 104, 105, 106, 107, 108],
    "name": ["Laptop", "Mouse", "Keyboard", "Monitor", "Webcam", "Headphones", "Microphone", "Speakers"],
    "category": ["Electronics", "Electronics", "Electronics", "Electronics", "Accessories", "Accessories", "Accessories", "Accessories"],
    "rate": [1200.00, 25.50, 75.00, 300.00, 50.00, 150.00, 80.00, 250.00],
    "description": [
        "High-performance laptop with a sleek design.",
        "Ergonomic wireless mouse with customizable buttons.",
        "Mechanical gaming keyboard with RGB backlighting.",
        "27-inch 4K UHD monitor with a fast refresh rate.",
        "Full HD webcam with built-in microphone for clear video calls.",
        "Noise-cancelling headphones for an immersive audio experience.",
        "Studio-quality condenser microphone for streaming and recording.",
        "Compact Bluetooth speakers with rich, powerful sound."
    ]
}
df = pd.DataFrame(products)

# --- Session State Initialization ---
if 'page' not in st.session_state:
    st.session_state.page = 'search'
if 'selected_product_id' not in st.session_state:
    st.session_state.selected_product_id = None
if 'search_results' not in st.session_state:
    st.session_state.search_results = pd.DataFrame()

# --- Mock API Functions ---
def mock_post_search(payload, headers):
    """
    Simulates a POST request to a search endpoint.
    In a real app, you would use requests.post() here.
    """
    # Simulate API call latency
    time.sleep(1) 
    
    # Check headers for authorization
    if 'Authorization' not in headers or headers['Authorization'] != 'Bearer my_secret_token':
        st.error("Authentication failed. Please check your headers.")
        return None

    # Filter data based on the payload (simulating server-side filtering)
    filtered_df = df.copy()
    if payload['category'] != "All":
        filtered_df = filtered_df[filtered_df['category'] == payload['category']]
    if payload['search_term']:
        search_term = payload['search_term'].lower()
        filtered_df = filtered_df[
            filtered_df['name'].str.lower().str.contains(search_term) | 
            filtered_df['description'].str.lower().str.contains(search_term)
        ]
    return filtered_df

def mock_get_product_details(product_id):
    """
    Simulates a GET request with a query string for a specific product.
    In a real app, you would use requests.get() here.
    """
    # Simulate API call latency
    time.sleep(0.5)

    try:
        product_details = df[df['product_id'] == product_id].iloc[0].to_dict()
        return product_details
    except IndexError:
        st.error(f"Product with ID {product_id} not found.")
        return None

# --- Page Functions ---
def search_page():
    """Displays the product search interface and results."""
    st.title("Product Search 🔍")
    st.markdown("Search for products by category and keywords.")

    with st.container(border=True):
        st.subheader("Search Criteria")
        col1, col2, col3 = st.columns([1, 2, 1])

        with col1:
            category = st.selectbox("Filter by Category", ["All"] + list(df['category'].unique()))
        
        with col2:
            search_term = st.text_input("Search by Name or Description", "")
        
        with col3:
            st.write("") # Spacer
            if st.button("Search", use_container_width=True):
                # Simulate the POST call
                payload = {"category": category, "search_term": search_term}
                headers = {"Authorization": "Bearer my_secret_token"}
                
                with st.spinner('Searching...'):
                    results_df = mock_post_search(payload, headers)
                
                st.session_state.search_results = results_df
                
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
                        st.experimental_rerun()
    else:
        if st.session_state.search_results is not None and len(st.session_state.search_results.index) == 0:
            st.info("No products found matching your criteria.")


def product_details_page():
    """Displays the detailed information for a single product."""
    st.subheader("Product Details")
    
    if st.session_state.selected_product_id is not None:
        # Simulate the GET call
        with st.spinner(f"Fetching details for ID {st.session_state.selected_product_id}..."):
            product_details = mock_get_product_details(st.session_state.selected_product_id)

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
                st.experimental_rerun()
    else:
        st.session_state.page = 'search'
        st.experimental_rerun()


# --- Main Application Logic ---
if st.session_state.page == 'search':
    search_page()
elif st.session_state.page == 'details':
    product_details_page()
