"""
This is a utility module.

To use this module, first import it:

import menu_process_file

This module supports moscow_codes_app programm
It contains functions that process work behind menu items of the programm

"""

import logging
import logging.handlers
import moscow_codes_app


def zip_by_location(codes, location):
    """
    This function searches for ZIP code(s) by given location
    
    Parameters
    ----------
    codes: list
        full ZIP codes list
    location: str
        location enetered by the user

    Returns
    ---------
    list    
    """
    zips = []
    for code in codes:
        if location.lower() == code[moscow_codes_app.area_column_index].lower().replace("район", "").strip():
            zips.append(code[moscow_codes_app.zip_column_index])
    return zips


def location_by_zip(codes, zipcode):
    """
    This function searches for location by given ZIP code  
    
    Parameters
    ----------
    codes: list
        full ZIP codes list
    zip_code: iterable
        ZIP code entered by user

    Returns
    ---------
    tuple
    
    Other functions involved
    ----------
    check_zip_input(zip_code)   
    """
    
    # Calling function that checks if entered ZIP code is correct
    zipcode = check_zip_input(zipcode)
    
    # Returning data behind ZIP code
    for code in codes:
        if code[moscow_codes_app.zip_column_index] == zipcode:
            return tuple(code)
    return ()
 
 
def check_zip_input(zip_code):
    """
    This function checks the adequacy of the entered number.
    If the number of figures is incorrect,
    the programm will allow user to enter the ZIP code again
    Parameters
    ----------
    zip_code: iterable
        ZIP code entered by user

    Returns
    ---------
    str
    """
    zip_code_length = 6
    while len(str(zip_code)) != zip_code_length:
        zip_code = input("Введите индекс, состоящий из 6 цифр: ").replace(" ", "")
    return zip_code