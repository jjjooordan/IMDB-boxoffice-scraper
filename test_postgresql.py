# test_postgresql.py
# Testing postgreSQL commands using psycopg2
# Ref. Development - IMDB Actor Filmography Jupyter Notebook for more details

import getpass
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import psycopg2
import sqlalchemy as sa
from IMDB_film_data import imdb_film_data
from IMDB_filmo_scraper import imdb_filmo_scraper

# Test actor: Tom Holland
href_actor = '/name/nm4043618/'
result_pd, name, dob = imdb_filmo_scraper(href_actor)

# Google Cloud Platform Parameters
db_user = "postgres"
db_host = "34.95.29.176"
db_name = "postgres"

# User inputs password and creates SQLAlchemy engine
db_pass = getpass.getpass("Password:")
conn = sa.create_engine("postgresql://postgres:" + db_pass + "@" + db_host + "/" + db_name)

# Clear and create temp_table
conn.execute(
    "DROP TABLE IF EXISTS temp_table"
)
conn.execute(
    "CREATE TABLE temp_table (href_filmact varchar PRIMARY KEY, href_film varchar, href_actor varchar, title varchar, year integer, imdb_rating numeric, imdb_qty integer, budget numeric, opening_wknd numeric, domestic_gross numeric, ww_gross numeric)"
)

# Populate temp_table with result_pd
# result_pd.to_sql("temp_table", conn, index = False, if_exists = 'append')
print("Create temp-table: Complete")

# Merge temp_table into db_actor
conn.execute(
    "INSERT INTO db_actor (href_actor, name, dob) VALUES (%s, %s, %s) ON CONFLICT (href_actor) DO NOTHING", (href_actor, name, dob)
    )

# Merge temp_table into db_film
conn.execute(
    sa.text("""\
        INSERT INTO db_film (href_film, title, year, imdb_rating, imdb_qty, budget, opening_wknd, domestic_gross, ww_gross)
        SELECT href_film, title, year, imdb_rating, imdb_qty, budget, opening_wknd, domestic_gross, ww_gross FROM temp_table
        ON CONFLICT (href_film) DO
            UPDATE SET (title, year, imdb_rating, imdb_qty, budget, opening_wknd, domestic_gross, ww_gross) = (EXCLUDED.title, EXCLUDED.year, EXCLUDED.imdb_rating, EXCLUDED.imdb_qty, EXCLUDED.budget, EXCLUDED.opening_wknd, EXCLUDED.domestic_gross, EXCLUDED.ww_gross)
        """
    )
)

# Merge temp_table into db_filmcredits
conn.execute(
    sa.text("""\
        INSERT INTO db_filmcredits (href_filmact, href_film, href_actor)
        SELECT href_filmact, href_film, href_actor FROM temp_table
        ON CONFLICT (href_filmact) DO NOTHING
        """
    )
)