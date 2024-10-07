from urllib.parse import urlparse, parse_qs, unquote


def get_center_lat_long(url):
    # Parse the URL
    parsed_url = urlparse(url)
    # Get the query string
    query_string = parsed_url.query
    # Parse the query parameters
    params = parse_qs(query_string)
    # Get the 'center' parameter
    center_values = params.get("center")
    if not center_values:
        return None  # or raise an exception if preferred
    center = center_values[0]
    # Decode URL-encoded characters
    center_decoded = unquote(center)
    # Split the center value into latitude and longitude
    lat_long = center_decoded.split(",")
    if len(lat_long) != 2:
        return None  # or raise an exception if preferred
    lat_str, long_str = lat_long
    # Convert strings to floats
    lat = float(lat_str)
    long = float(long_str)
    # Return the result in a dictionary
    return {"lat": lat, "long": long}


url = "https://maps.googleapis.com/maps/api/staticmap?size=742x330&center=40.38543040%2C-3.69652730&maptype=roadmap&channel=map_detail&scale=2&zoom=16&key=...&markers=...&signature=..."

result = get_center_lat_long(url)
print(result)  # Output: {'lat': 40.3854304, 'long': -3.6965273}
