"""
This is a configuration file for a program that shows US farmer markets.
It opens a connection with MSSQL database
"""


import pyodbc

server = 'LAPTOP-9NI9ES32\SQLEXPRESS' 
database = 'Farmers'
username = 'OlgaP'
password = 'rsb4243'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)