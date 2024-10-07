from urllib.parse import urlparse, parse_qs, unquote


def get_center_lat_long(url):
    parsed_url = urlparse(url)
    query_string = parsed_url.query
    params = parse_qs(query_string)
    center_values = params.get("center")
    if not center_values:
        return None
    center = center_values[0]
    center_decoded = unquote(center)
    lat_long = center_decoded.split(",")
    if len(lat_long) != 2:
        return None
    lat_str, long_str = lat_long
    lat = float(lat_str)
    long = float(long_str)
    return lat, long
