import mysql.connector
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
import pandas as pd

#pip install pandas openpyxl load_dotenv mysql-connector-python

load_dotenv()
DATABASE_URI = os.getenv('DB_MYSQL')
SECRET_KEY = os.getenv('FLASK_SECRET_KEY') or os.getenv('CSRF_SECRET')

def connect_to_db():
    try:
        # Parse the URL to extract components
        parsed_url = urlparse(DATABASE_URI)
        db_user = parsed_url.username
        db_password = parsed_url.password
        db_host = parsed_url.hostname
        db_port = parsed_url.port if parsed_url.port else 3306  # Default MySQL port
        db_name = parsed_url.path.strip('/')
    
        # Establish the connection
        connection = mysql.connector.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database=db_name
        )
    
        if connection.is_connected():
            db_info = connection.server_info
            print(f"Connected to MySQL Server version {db_info}")
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print(f"You're connected to database: {record}")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def read_spreadsheet():
    # Specify the path to your XLSX file
    excel_file_path = 'C:/Users/alexv/workspace/parse-spreadsheet/915nebaseballwebsitedata.xlsx' 
    
    # Read the Excel file into a Pandas DataFrame
    df = pd.read_excel(excel_file_path)
    
    # Display the first few rows of the DataFrame
    print(df.head())
    
    xls = pd.ExcelFile(excel_file_path)
    sheet_names = xls.sheet_names
    print(sheet_names)
    
    df = pd.read_excel(excel_file_path, sheet_name='Coaches & Team Moms') # Read by sheet name
    #df = pd.read_excel(excel_file_path, sheet_name=3) # Read by sheet index (0-indexed)
    
    # Display the first few rows of the DataFrame
    print(df.head())

connect_to_db()


