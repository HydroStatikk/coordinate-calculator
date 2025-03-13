import math

def validate_coordinates(lat1, lon1, lat2, lon2):
    """
    Validate coordinates to ensure they are within valid ranges and are numeric.
    
    Args:
        lat1, lon1, lat2, lon2: Coordinate values as strings
    
    Returns:
        Error message if validation fails, None otherwise
    """
    try:
        # Check if all values are provided
        if not all([lat1, lon1, lat2, lon2]):
            return "All coordinate fields are required."
        
        # Convert to float and check if conversion is successful
        lat1_float, lon1_float = float(lat1), float(lon1)
        lat2_float, lon2_float = float(lat2), float(lon2)
        
        # Validate latitude range (-90 to 90)
        if not (-90 <= lat1_float <= 90) or not (-90 <= lat2_float <= 90):
            return "Latitude must be between -90 and 90 degrees."
            
        # Validate longitude range (-180 to 180)
        if not (-180 <= lon1_float <= 180) or not (-180 <= lon2_float <= 180):
            return "Longitude must be between -180 and 180 degrees."
            
        return None
    except ValueError:
        return "All coordinates must be valid numbers."

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the Haversine distance between two points on the earth.
    
    Args:
        lat1, lon1: Latitude and longitude of point 1 in decimal degrees
        lat2, lon2: Latitude and longitude of point 2 in decimal degrees
    
    Returns:
        Distance in kilometers
    """
    # Radius of the Earth in kilometers
    R = 6371.0
    
    # Convert decimal degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Difference in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    
    return distance

def format_distance(distance):
    """
    Format distance to display with 2 decimal places.
    
    Args:
        distance: Distance value
    
    Returns:
        Formatted distance string
    """
    return f"{distance:.2f}"
