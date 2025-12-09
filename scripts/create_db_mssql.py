import os
import sys
import pyodbc
from decouple import config

def main():
    server = config('DB_HOST', default='127.0.0.1')
    username = config('DB_USER', default='')
    password = config('DB_PASSWORD', default='')
    db_name = config('DB_NAME', default='HR_System')
    driver = os.getenv('ODBC_DRIVER', 'ODBC Driver 17 for SQL Server')

    conn_str = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"UID={username};PWD={password};"
        "DATABASE=master;"
        "TrustServerCertificate=yes;"
    )

    print(f"Connecting to SQL Server {server} as {username}...")
    try:
        conn = pyodbc.connect(conn_str, timeout=10)
    except Exception as e:
        print("Connection failed:", e)
        sys.exit(1)

    try:
        cursor = conn.cursor()
        cursor.execute(f"IF DB_ID('{db_name}') IS NULL CREATE DATABASE [{db_name}]")
        conn.commit()
        print(f"Database ensured: {db_name}")
    except Exception as e:
        print("Error creating database:", e)
        sys.exit(2)
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    main()
