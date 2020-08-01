# IMDB_filmo_scaper.py
# Ref. Development - IMDB Actor Filmography Jupyter Notebook for more details

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from IMDB_film_data import imdb_film_data

def imdb_filmo_scraper(actor_href):
    
    # Append href input to full IMDB URL
    imdbUrl = 'https://www.imdb.com' + actor_href

    # Parse URL with BeautifulSoup
    r = requests.get(imdbUrl)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    # Retrieve Actor or Actress name
    imdbNameData = soup.find('div', id = 'name-overview-widget')
    fullname = imdbNameData.h1.text.strip()
    
    # Retrieve birthday
    imdbBirthday = soup.find('time')
    birthday = imdbBirthday.get('datetime')

    # Retrieve filmography data
    # Revised for Actor and Actress credits
    films = soup.find_all('div', id = re.compile('^act'))
    
    # Create array, append what each href returns from IMDB Film Data function, then convert array to DataFrame 
    filmsarray = []
    for film in films:
        film_href = film.a.get('href')
        filmsarray.append(actor_href, imdb_film_data(film_href))
    
    filmspd = pd.DataFrame(filmsarray, columns = ['actor_href',
                                                  'film_href',
                                                  'Title',
                                                  'Year',
                                                  'IMDB_Rating',
                                                  '#_of_Ratings',
                                                  'Budget',
                                                  'Opening_Weekend',
                                                  'Domestic_Gross',
                                                  'Worldwide_Gross'
                                                 ])

    return filmspd, fullname, birthday
