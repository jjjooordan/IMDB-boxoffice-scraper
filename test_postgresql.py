# test_postgresql.py
# Testing postgreSQL commands using psycopg2
# Ref. Development - IMDB Actor Filmography Jupyter Notebook for more details

import getpass
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import psycopg2
from IMDB_film_data import imdb_film_data
# from configobj import ConfigObj

# Configure PostgreSQL DB parameters:
db_host = "localhost"
db_name = "Supermart_DB"
db_user = "postgres"
db_port = "5432"

# Connect to PostgreSQL DB:
try:
    conn = psycopg2.connect(
        host = db_host,
        database = db_name,
        user = db_user,
        password = getpass.getpass("Password:"),
        port = db_port
    )
    print("Database successfully connected.")

except:
    print("Database failed to connect.")

# Create cursor
cur = conn.cursor()

# Execute query
cur.execute("SELECT customer_id, customer_name FROM customer LIMIT 100;")

# Get everything
rows = cur.fetchall()

for r in rows:
    print(r)

# Commit transaction
conn.commit()

# Close cursor and connection
cur.close()
conn.close()
