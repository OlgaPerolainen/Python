"""
This is a utility module.

To use this module, first import it:

import read_postal_codes

Use the read_zip_all() function to read the data
on ZIP codes:

zip_codes = read_postal_codes.read_zip_all()
print(zip_codes[101000])
"""


def read_zip_all():
    """
    This function reads ZIP codes from a file and adds them to list
    that would be used by the programm
    
    Check db_file_name, lat_column_name, longit_column_name
    if you change the database

    Returns
    ---------
    list
        contains all ZIP codes from a given file
    """
    
    row = 0
    header = []
    zip_codes = []
    zip_data = [] 
    skip_line = False
    db_file_name = "moscow_postal_codes.csv"
    lat_column_name = "Y_WGS84"
    longit_column_name = "X_WGS84"
    
    # Open file with ZIP codes and data
    for line in open(db_file_name).read().split("\n"):
        skip_line = False
        entry = line.strip().split(";")                    
        row += 1
        
        # Add headers to list "header"
        if row == 1:
            for val in entry:
                header.append(val)
        
        # Add all other data to list "zip_codes"
        else:
            zip_data = []                          # list of data for every ZIP code
            for index in range(0, len(entry)):
                if entry[index] == '':
                    skip_line = True
                    break
                    
                # Convert geographic coordinates to float
                if header[index] == lat_column_name or header[index] == longit_column_name:
                    val = float(entry[index].replace(",", "."))
                else:
                    val = entry[index]
                zip_data.append(val)
            if not skip_line:
                zip_codes.append(zip_data)
    return zip_codes