import pyodbc
from getpass import getpass
from subprocess import Popen, PIPE, STDOUT
import webbrowser
import textwrap
 

SQL_SCRIPT = r'farmer_market_app/data/farmers_data.sql'
config_file = r'farmer_market_app/source/config.py'
app_start_file = r'farmer_market_app/market_app.py'


def populate_database(db_name, script):
    """
    This function runs the script that creates tables and inserts data
    
    Parameters
    ----------
    db_name: str
        name of a database
    script: str
        path to a file with script

    Returns
    ---------
    None or str
    """
    commands = []
    with connection.cursor() as cursor:
        cursor.execute(f'USE {db_name};')
        with open(script,'r') as inserts:
            sqlScript = inserts.read()
            query_string = textwrap.dedent("""{}""".format(sqlScript))
            for statement in query_string.split('GO;;'):
                commands.append(statement + ';')
            for command in commands:
                try:
                    cursor.execute(command)
                except pyodbc.Error as err:
                    print(f'Error occured while executing sql script')
                    print(err)


# Checking that user has MSSQL and pyodbc module
if input('This application is working with MSSQL.\n' +
         'Make sure you have pyodbc module installed.\n' +
         'Continue? [y/n]: ').lower() == 'y':
    
    # Getting data for connection
    server = input('Enter the server name of your MSSQL instance: ') 
    username = input('Enter the username of your MSSQL instance: ')
    password = getpass(f'Enter the password for user {username}: ')
    database = input('Enter the name of the database to be created or used: ')
        
    # Connecting to MSSQL
    try:
        connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';UID='+username+';PWD='+ password)
        print('Connected to SQL Server Successfully')

        with connection.cursor() as cursor:
            # Checking that this database exists
            try:
                cursor.execute(f'USE {database};')
                print(f"Connecting to database {database}")
            except:
                print("----------------------------" +
                      f"\nDatabase {database} not found.\nWe recommend choosing full deployment." +
                      "\nOtherwise, you'll quit the application" +
                      "\n----------------------------")

        # Full deployment
        if input('Full deployment? [y/n]: ').lower() == 'y':
            connection.autocommit = True

            # Creating new database
            with connection.cursor() as cursor:
                try:
                    cursor.execute(f"USE master;")
                    cursor.execute(f"CREATE DATABASE {database};")
                    print(f"{database} database is created." +
                            "\nUploading data...")
                    populate_database(database, SQL_SCRIPT)
                                                       
                except pyodbc.DatabaseError as err:
                    if err.args[0] == '42000':
                        if input(f'Database {database} already exists. Do you want to drop it? [y/n]: ') == 'y':
                            cursor.execute(f"USE master;")
                            cursor.execute(f"DROP DATABASE {database};")
                            cursor.execute(f"CREATE DATABASE {database};")
                            print(f'Database {database} is dropped and created anew.\nUploading data...')
                            populate_database(database, SQL_SCRIPT)
        
        # Fast deployment        
        else:
            print("Using the old version of database.")
            try:
                cursor.execute(f'USE {database};')
            except:
                print("Aborting deployment")
                raise SystemExit

        connection.close()  
        
        # Changing configuration file       
        with open(config_file, "r") as f:
            try:
                data = f.read()
                data = data.replace("username = 'username'", f"username = '{username}'") \
                    .replace("password = 'password'", f"password = '{password}'") \
                    .replace("server = 'server'",
                            f"server = '{server}'") \
                    .replace("database = 'database'", f"database = '{database}'")
                with open(config_file, "w") as f:
                    f.write(data)
            except:
                print(f'Error occured while working with config file.')
                raise SystemExit
                            

        # Running app and creating log files
        with open('test.log','wb') as out, open('test-error.log','wb') as err:
            p = Popen(['python', app_start_file], stdout=out, stderr=err)

        # Running webbrowser          
        webbrowser.open('http://127.0.0.1:5000/', new=2)

    except:
        print('Connection to MSSQL failed')    

