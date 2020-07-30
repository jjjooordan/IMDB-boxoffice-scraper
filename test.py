import getpass
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import psycopg2
from IMDB_film_data import imdb_film_data
from IMDB_filmo_scraper import imdb_filmo_scraper


actor_href = 'act-123123'
film_href = 'film-123123'
title = 'Top Gun'
year = 1990
imdb_rating = 9.9
rating_qty = 100
budget = 100
opening_wknd = 200
domestic_gross = 300
ww_gross = 400
filmact_id = actor_href + film_href


imdb_filmo_scraper('/nm0000129/')