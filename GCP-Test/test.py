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
    "CREATE TABLE temp_table_film (filmact_id varchar PRIMARY KEY, actor_href varchar, film_href varchar, title varchar, year integer, imdb_rating numeric, rating_qty numeric, budget numeric, opening_wknd numeric, domestic_gross numeric, ww_gross numeric)"
)
print("Created temp_table_film.")

# Clear and create temp_table_actor
print("Creating temp_table_actor.")
conn.execute(
    "DROP TABLE IF EXISTS temp_table_actor"
)
conn.execute(
    "CREATE TABLE temp_table_actor (actor_href varchar PRIMARY KEY, fullname varchar NOT NULL, dob DATE)"
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
        INSERT INTO db_film (film_href, title, year, imdb_rating, rating_qty, budget, opening_wknd, domestic_gross, ww_gross)
        SELECT film_href, title, year, imdb_rating, rating_qty, budget, opening_wknd, domestic_gross, ww_gross FROM temp_table_film
        ON CONFLICT (film_href) DO
            UPDATE SET (title, year, imdb_rating, rating_qty, budget, opening_wknd, domestic_gross, ww_gross) = (EXCLUDED.title, EXCLUDED.year, EXCLUDED.imdb_rating, EXCLUDED.rating_qty, EXCLUDED.budget, EXCLUDED.opening_wknd, EXCLUDED.domestic_gross, EXCLUDED.ww_gross)
        """
    )
)
print("Upsert to db_film complete.")

# Merge temp_table_actor into db_actor
conn.execute(
    sa.text("""\
        INSERT INTO db_actor (actor_href, fullname, dob)
        SELECT actor_href, fullname, dob FROM temp_table_actor
        ON CONFLICT (actor_href) DO NOTHING
        """
    )
)
print("Upsert to db_filmcredits complete.")

# Merge temp_table_film into db_filmcredits
conn.execute(
    sa.text("""\
        INSERT INTO db_filmcredits (filmact_id, film_href, actor_href)
        SELECT filmact_id, film_href, actor_href FROM temp_table_film
        ON CONFLICT (filmact_id) DO NOTHING
        """
    )
)
print("Upsert to db_filmcredits complete.")
