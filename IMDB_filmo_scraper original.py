# IMDB_filmo_scaper.py
# Ref. Development - IMDB Actor Filmography Jupyter Notebook for more details
# imdb_filmo_scraper(href_actor)
# Returns DataFrame, full name, date of birth

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from IMDB_film_data import imdb_film_data

def imdb_filmo_scraper(href_actor):
    
    # Append href input to full IMDB URL
    imdbUrl = 'https://www.imdb.com' + href_actor

    # Parse URL with BeautifulSoup
    r = requests.get(imdbUrl)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    # Retrieve Actor or Actress name
    imdbNameData = soup.find('td', class_ = 'name-overview-widget__section')
    imdbName = imdbNameData.find('span', class_ = 'itemprop')
    fullname = imdbName.text
    
    # Retrieve birthday
    imdbBirthdaytag = soup.find('div', id = 'name-born-info')
    imdbBirthday = imdbBirthdaytag.find('time')
    dob = imdbBirthday.get('datetime')
    
    # Retrieve filmography data
    # Revised for Actor and Actress credits
    films = soup.find_all('div', id = re.compile('^act'))
    
    # Create array, append what each href returns from IMDB Film Data function, then convert array to DataFrame 
    filmsarray = []
    for film in films:
        href_film = film.a.get('href')
        filmsarray.append(href_actor, imdb_film_data(href_film))
    
    filmspd = pd.DataFrame(filmsarray, columns = ['href_actor',
                                                  'href_film',
                                                  'title',
                                                  'year',
                                                  'imdb_rating',
                                                  'imdb_qty',
                                                  'budget',
                                                  'opening_wknd',
                                                  'domestic_gross',
                                                  'ww_gross'
                                                 ])

    return filmspd, fullname, dob
