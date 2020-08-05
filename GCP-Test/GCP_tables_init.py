import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import psycopg2
import getpass
import sqlalchemy as sa

# Upload DataFrame to Google Cloud Platform
# Google Cloud Platform Parameters
db_user = "postgres"
db_host = "34.95.29.176"
db_name = "postgres"

# User inputs password and creates SQLAlchemy engine
db_pass = getpass.getpass("Password:")
conn = sa.create_engine("postgresql://postgres:" + db_pass + "@" + db_host + "/" + db_name)
print("Connected to Google Cloud Platform.")

# Clear existing temp_tablefilmdata and temp_tableactordata tables
print("Dropping temp_table.")
conn.execute(
    "DROP TABLE IF EXISTS temp_table CASCADE"
)
print("Dropped temp_table.")
print("Dropping temp_tablefilm.")
conn.execute(
    "DROP TABLE IF EXISTS temp_tablefilm CASCADE"
)
print("Dropped temp_table_film.")
print("Dropping temp_table_actor.")
conn.execute(
    "DROP TABLE IF EXISTS temp_table_actor CASCADE"
)
print("Dropped temp_table_actor.")

# Clear existing db_filmcredits, db_actor, and db_film tables
print("Dropping film_credits.")
conn.execute(
    "DROP TABLE IF EXISTS film_credits CASCADE"
)
print("Dropped film_credits.")
print("Dropping db_filmcredits.")
conn.execute(
    "DROP TABLE IF EXISTS db_filmcredits CASCADE"
)
print("Dropped db_filmcredits.")
print("Dropping db_actor.")
conn.execute(
    "DROP TABLE IF EXISTS db_actor CASCADE"
)
print("Dropped db_actor.")
print("Dropping db_film.")
conn.execute(
    "DROP TABLE IF EXISTS db_film CASCADE"
)
print("Dropped db_film.")

# Create db_actor
print("Creating db_actor.")
conn.execute(
    "CREATE TABLE db_actor (actor_href varchar PRIMARY KEY, fullname varchar NOT NULL, dob date)"
)
print("Created db_actor.")

# Create db_film
print("Creating db_film.")
conn.execute(
    "CREATE TABLE db_film (film_href varchar PRIMARY KEY, title varchar NOT NULL, year integer, imdb_rating numeric, rating_qty numeric, budget numeric, opening_wknd numeric, domestic_gross numeric, ww_gross numeric)"
)
print("Created db_film.")

# Create db_filmcredits
print("Creating db_filmcredits.")
conn.execute(
    "CREATE TABLE db_filmcredits (filmact_id varchar PRIMARY KEY, film_href varchar REFERENCES db_film, actor_href varchar REFERENCES db_actor)"
)
print("Created db_filmcredits.")
