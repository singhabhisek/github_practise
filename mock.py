# api.py

from flask import Flask, jsonify, request
from flask_cors import CORS # This is crucial for local development

app = Flask(__name__)
CORS(app) # Enable Cross-Origin Resource Sharing for the Streamlit app

# --- Sample Data ---
products = {
    101: {"product_id": 101, "name": "Laptop", "category": "Electronics", "rate": 1200.00, "description": "High-performance laptop with a sleek design."},
    102: {"product_id": 102, "name": "Mouse", "category": "Electronics", "rate": 25.50, "description": "Ergonomic wireless mouse with customizable buttons."},
    103: {"product_id": 103, "name": "Keyboard", "category": "Electronics", "rate": 75.00, "description": "Mechanical gaming keyboard with RGB backlighting."},
    104: {"product_id": 104, "name": "Monitor", "category": "Electronics", "rate": 300.00, "description": "27-inch 4K UHD monitor with a fast refresh rate."},
    105: {"product_id": 105, "name": "Webcam", "category": "Accessories", "rate": 50.00, "description": "Full HD webcam with built-in microphone for clear video calls."},
    106: {"product_id": 106, "name": "Headphones", "category": "Accessories", "rate": 150.00, "description": "Noise-cancelling headphones for an immersive audio experience."},
    107: {"product_id": 107, "name": "Microphone", "category": "Accessories", "rate": 80.00, "description": "Studio-quality condenser microphone for streaming and recording."},
    108: {"product_id": 108, "name": "Speakers", "category": "Accessories", "rate": 250.00, "description": "Compact Bluetooth speakers with rich, powerful sound."}
}

@app.route('/search', methods=['POST'])
def search_products():
    """Endpoint for searching products with POST request."""
    # Verify the Authorization header
    if request.headers.get('Authorization') != 'Bearer my_secret_token':
        return jsonify({"error": "Unauthorized"}), 401

    payload = request.json
    category = payload.get('category', 'All')
    search_term = payload.get('search_term', '').lower()

    filtered_products = [
        p for p in products.values()
        if (category == 'All' or p['category'] == category) and
           (not search_term or search_term in p['name'].lower() or search_term in p['description'].lower())
    ]

    return jsonify(filtered_products)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product_details(product_id):
    """Endpoint for fetching a single product's details with a GET request."""
    product = products.get(product_id)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
