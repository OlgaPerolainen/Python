"""
This is a utility module.

To use this module, first import it:

import geo_formulas

Use calculate_distance(location1, location2) function
to calculate distance between to points:

distance = geo_formulas.calculate_distance((latitude1, longitude1),
                                            (latitude2, longitude2))
"""

import math


def calculate_delta_devided_by_two(parameter1, parameter2):
    return ((parameter1 - parameter2) / 2)


def calculate_distance(location1, location2):
    """
    This function returns the great-circle distance between location1 and
    location2.

    Parameters
    ----------
    location1: iterable
        geographic coordinates
        index 0 stands for latitude
        index 1, for longitude

    location2: iterable
        geographic coordinates
        index 0 stands for latitude
        index 1, for longitude

    Returns
    ----------
    float
        Value of the distance between two locations computed using
        the haversine formula
    """
    
    earth_radius_km = 6371.008
    
    lat1 = math.radians(location1[0])
    lat2 = math.radians(location2[0])
    long1 = math.radians(location1[1])
    long2 = math.radians(location2[1])
    del_lat = calculate_delta_devided_by_two(lat1, lat2)
    del_long = calculate_delta_devided_by_two(long1, long2)
    angle = math.sin(del_lat)**2 + math.cos(lat1) * math.cos(lat2) * \
        math.sin(del_long)**2
    distance = 2 * earth_radius_km * math.asin(math.sqrt(angle))
    return distance

def cardinal_directions(location):
    """
    This function computes wether it is south or north latitude
    and west or east longitude of given geographic coordinates
    
    Parameters
    ----------
    location: iterable
        geographic coordinates
        index 0 stands for latitude
        index 1, for longitude

    Returns
    ---------
    tuple
        contains computed cardinal directions
    """
    
    # Computing wether it is south or north latitude 
    ns = ""
    if location[0] < 0:
        ns = 'S'
    elif location[0] >= 0:
        ns = 'N'

    # Computing wether it is west or east longitude 
    ew = ""
    if location[1] < 0:
        ew = 'W'
    elif location[1] >= 0:
        ew = 'E'
    
    return (ns, ew)


def degree_minutes_seconds(location):
    """
    This function calculates degrees, minutes and seconds of geographic coordinates
    
    Parameters
    ----------
    location: iterable
        geographic coordinates
        index 0 stands for latitude
        index 1, for longitude

    Returns
    ---------
    tuple
        contains calculated degrees, minutes, seconds
    """
    minutes_in_degree = 60
    seconds_in_minute = 60
    
    minutes, degrees = math.modf(location)
    degrees = int(degrees)
    minutes *= minutes_in_degree
    seconds, minutes = math.modf(minutes)
    minutes = int(minutes)
    seconds *= seconds_in_minute
    return degrees, minutes, seconds


def format_location(location):
    """
    This function formats the value of geographic coordinates
    
    Parameters
    ----------
    location: iterable
        geographic coordinates
        index 0 stands for latitude
        index 1, for longitude

    Returns
    ---------
    str
    
    Other functions involved
    ----------
    cardinal_directions(location)
    degree_minutes_seconds(location):
    """
    
    # Calling function that computes wether it is south or north latitude 
    # and west or east longitude 
    ns, ew = cardinal_directions(location)

    format_string = '{:03d}\xb0{:0d}\'{:.2f}"'
    
    # Calling function that calculates degrees, minutes and seconds of geographic coordinates
    lat_degree, lat_min, lat_secs = degree_minutes_seconds(abs(location[0]))
    latitude = format_string.format(lat_degree, lat_min, lat_secs)
    
    # Calling function that calculates degrees, minutes and seconds of geographic coordinates 
    long_degree, long_min, long_secs = degree_minutes_seconds(abs(location[1]))
    longitude = format_string.format(long_degree, long_min, long_secs)
    
    return '(' + latitude + ns + ',' + longitude + ew + ')'