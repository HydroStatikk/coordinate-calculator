import os
import logging
from flask import Flask, render_template, request, jsonify
from coordinates import calculate_distance, validate_coordinates, format_distance

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")

# Store recent calculations
recent_calculations = []

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html', recent_calculations=recent_calculations)

@app.route('/calculate', methods=['POST'])
def calculate():
    """Calculate distance between two coordinate points."""
    try:
        # Get coordinates from form data
        lat1 = request.form.get('lat1')
        lon1 = request.form.get('lon1')
        lat2 = request.form.get('lat2')
        lon2 = request.form.get('lon2')

        # Validate coordinates
        error = validate_coordinates(lat1, lon1, lat2, lon2)
        if error:
            return jsonify({"success": False, "error": error})

        # Convert coordinates to float
        lat1, lon1, lat2, lon2 = float(lat1), float(lon1), float(lat2), float(lon2)

        # Calculate distance
        distance_km = calculate_distance(lat1, lon1, lat2, lon2)
        distance_mi = distance_km * 0.621371

        # Format the results
        result = {
            "success": True,
            "point1": f"({lat1}, {lon1})",
            "point2": f"({lat2}, {lon2})",
            "distance_km": format_distance(distance_km),
            "distance_mi": format_distance(distance_mi)
        }

        # Add to recent calculations (limit to 5)
        recent_calculations.insert(0, result)
        if len(recent_calculations) > 5:
            recent_calculations.pop()

        return jsonify(result)
    except Exception as e:
        logging.error(f"Error calculating distance: {str(e)}")
        return jsonify({"success": False, "error": "An unexpected error occurred."})
