import getpass
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import psycopg2
from IMDB_film_data import imdb_film_data
from configobj import ConfigObj

config_db = ConfigObj('config_data.ini')

test = config_db('db_host')
print(test)


# try:
#     conn = psycopg2.connect(
#         host = config_db(db_host),
#         database = config_db(db_name),
#         user = config_db(db_user),
#         password = getpass.getpass("Password:"),
#         port = config_db(db_port)
#     )
#     print("Database successfully connected.")