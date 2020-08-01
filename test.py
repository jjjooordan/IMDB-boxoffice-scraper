import getpass
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import psycopg2
from IMDB_film_data import imdb_film_data
from IMDB_filmo_scraper import imdb_filmo_scraper

actor_href = '/name/nm0000129/'
    
# Append href input to full IMDB URL
imdbUrl = 'https://www.imdb.com' + actor_href

# Parse URL with BeautifulSoup
r = requests.get(imdbUrl)
soup = BeautifulSoup(r.content, 'html.parser')

# Retrieve filmography data
# Revised for Actor and Actress credits
films = soup.find_all('div', id = re.compile('^act'))

# Retrieve Actor or Actress name
imdbNameData = soup.find('div', id = 'name-overview-widget')
fullname = imdbNameData.h1.text.strip()

# Retrieve birthday
imdbBirthday = soup.find('time')
birthday = imdbBirthday.get('datetime')

print(fullname, birthday)

# imdbFilmdata = soup.find('div', class_ = 'title_wrapper')
# title_year = imdbFilmdata.h1.text
# if imdbFilmdata.h1.span is None:
#     title_year = title_year.replace(u'\xa0',u' ')
#     title = title_year.strip()
#     year = None
#     pass
# else:
#     yearbrackets = imdbFilmdata.h1.span.text
#     title = title_year[:-len(yearbrackets)-2]
#     yearstr = yearbrackets[1:len(yearbrackets)-1]
#     year = int(yearstr)