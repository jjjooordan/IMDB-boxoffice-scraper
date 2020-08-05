# Test.py
# Hard-coded example to pull filmography data of Tom Holland and upload to Google Cloud Platform Cloud SQL server

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import psycopg2
import getpass
import sqlalchemy as sa


# Create DataFrame to upload
from IMDB_filmo_scraper import imdb_filmo_scraper
from IMDB_film_data import imdb_film_data
from usd_conversion import usd_conversion

# Example: Tom Holland
result_films, result_actor = imdb_filmo_scraper('/name/nm4043618/')
print("Results created.")

# Upload DataFrame to Google Cloud Platform
# Google Cloud Platform Parameters
db_user = "postgres"
db_host = "34.95.29.176"
db_name = "postgres"

# User inputs password and creates SQLAlchemy engine
db_pass = getpass.getpass("Password:")
conn = sa.create_engine("postgresql://postgres:" + db_pass + "@" + db_host + "/" + db_name)
print("Connected to Google Cloud Platform.")

# Clear and create temp_table_film
print("Creating temp_table_film.")
conn.execute(
    "DROP TABLE IF EXISTS temp_table_film"
)
conn.execute(
    "CREATE TABLE temp_table_film (key_filmact varchar PRIMARY KEY, href_actor varchar, href_film varchar, title varchar, year integer, imdb_rating numeric, imdb_qty numeric, budget numeric, gross_wknd numeric, gross_domestic numeric, gross_ww numeric)"
)
print("Created temp_table_film.")

# Clear and create temp_table_actor
print("Creating temp_table_actor.")
conn.execute(
    "DROP TABLE IF EXISTS temp_table_actor"
)
conn.execute(
    "CREATE TABLE temp_table_actor (href_actor varchar PRIMARY KEY, fullname varchar NOT NULL, dob DATE)"
)

# Populate temp_table_film with result_films
result_films.to_sql("temp_table_film", conn, index = False, if_exists = 'append')
print("Populated temp_table_film.")

# Populate temp_table_actor with result_actor
result_actor.to_sql("temp_table_actor", conn, index = False, if_exists = 'append')
print("Populated temp_table_actor.")

# Merge temp_table_film into db_film
conn.execute(
    sa.text("""\
        INSERT INTO db_film (href_film, title, year, imdb_rating, imdb_qty, budget, gross_wknd, gross_domestic, gross_ww)
        SELECT href_film, title, year, imdb_rating, imdb_qty, budget, gross_wknd, gross_domestic, gross_ww FROM temp_table_film
        ON CONFLICT (href_film) DO
            UPDATE SET (title, year, imdb_rating, imdb_qty, budget, gross_wknd, gross_domestic, gross_ww) = (EXCLUDED.title, EXCLUDED.year, EXCLUDED.imdb_rating, EXCLUDED.imdb_qty, EXCLUDED.budget, EXCLUDED.gross_wknd, EXCLUDED.gross_domestic, EXCLUDED.gross_ww)
        """
    )
)
print("Upsert to db_film complete.")

# Merge temp_table_actor into db_actor
conn.execute(
    sa.text("""\
        INSERT INTO db_actor (href_actor, fullname, dob)
        SELECT href_actor, fullname, dob FROM temp_table_actor
        ON CONFLICT (href_actor) DO NOTHING
        """
    )
)
print("Upsert to db_filmcredits complete.")

# Merge temp_table_film into db_filmcredits
conn.execute(
    sa.text("""\
        INSERT INTO db_filmcredits (key_filmact, href_film, href_actor)
        SELECT key_filmact, href_film, href_actor FROM temp_table_film
        ON CONFLICT (key_filmact) DO NOTHING
        """
    )
)
print("Upsert to db_filmcredits complete.")
