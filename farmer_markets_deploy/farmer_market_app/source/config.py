"""
This is a configuration file for a program that shows US farmer markets.
It opens a connection with MSSQL database
"""


import pyodbc

server = 'server' 
database = 'database'
username = 'username'
password = 'password'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)