# IMDB_filmo_scraper.py
# Ref. Development - IMDB Actor Filmography Jupyter Notebook for more details
# Input: imdb_filmo_scraper(href_actor)
# Output: filmspd, actorpd
# Where filmspd is a DataFrame with data outputs from IMDB_film_data.py
#       actorpd is a DataFrame with href_actor, fullname, dob data

import datetime
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from IMDB_film_data import imdb_film_data

def imdb_filmo_scraper(href_actor):
#     # Function timing
#     filmostart = pd.Timestamp.now()
#     print('IMDB Filmography Time Start!')
    
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
    str_dob = imdbBirthday.get('datetime')
    dob = datetime.datetime.strptime(str_dob, '%Y-%m-%d')

    # Create array for actor data, then convert to DataFrame
    actorpd = pd.DataFrame({"href_actor" : [href_actor],
                               "fullname" : [fullname],
                               "dob" : [dob]})

    # Retrieve filmography data
    # Revised for Actor and Actress credits
    films = soup.find_all('div', id = re.compile('^act'))
    
#     # Time milestone - Site parse time
#     siteparsetime = pd.Timestamp.now()
#     print('Site parsed - Time elapsed:')
#     print(siteparsetime - filmostart)

#     startfilmoprocessing = pd.Timestamp.now()

    # Create array, append what each href returns from IMDB Film Data function, then convert array to DataFrame 
    filmsarray = []
    for film in films:
        href_film = film.a.get('href')
        film_row = imdb_film_data(href_film)
        film_row.insert(0, href_actor)
        key_filmact = href_film + href_actor
        film_row.insert(0, key_filmact)
        filmsarray.append(film_row)
        
#         # Time milestone - Each film iteration in array
#         print('Film processed:')
#         print(pd.Timestamp.now())
        
    filmspd = pd.DataFrame(filmsarray, columns = ['key_filmact',
                                                  'href_actor',
                                                  'href_film',
                                                  'title',
                                                  'year',
                                                  'imdb_rating',
                                                  'imdb_qty',
                                                  'budget',
                                                  'gross_wknd',
                                                  'gross_domestic',
                                                  'gross_ww'
                                                  ])
#     # Time milestone - Filmography processing done
#     print('Total time:')
#     print(pd.Timestamp.now() - filmostart)
    return filmspd, actorpd
