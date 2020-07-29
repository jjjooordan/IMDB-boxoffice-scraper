# IMDB_filmo_scaper.py
# Ref. Development - IMDB Actor Filmography Jupyter Notebook for more details

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from IMDB_film_data import imdb_film_data

def imdb_filmo_scraper(actor_href):
#     # Function timing
#     filmostart = pd.Timestamp.now()
#     print('IMDB Filmography Time Start!')
    
    # Append href input to full IMDB URL
    imdbUrl = 'https://www.imdb.com' + actor_href

    # Parse URL with BeautifulSoup
    r = requests.get(imdbUrl)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    # Retrieve filmography data
    films = soup.find_all('div', id = re.compile('^act-'))
    
#     # Time milestone - Site parse time
#     siteparsetime = pd.Timestamp.now()
#     print('Site parsed - Time elapsed:')
#     print(siteparsetime - filmostart)

#     startfilmoprocessing = pd.Timestamp.now()

    # Create array, append what each href returns from IMDB Film Data function, then convert array to DataFrame 
    filmsarray = []
    for film in films:
        film_href = film.a.get('href')
        filmsarray.append(imdb_film_data(film_href))
        
#         # Time milestone - Each film iteration in array
#         print('Film processed:')
#         print(pd.Timestamp.now())
        
    filmspd = pd.DataFrame(filmsarray, columns = ['Title',
                                                  'Year',
                                                  'IMDB_Rating',
                                                  '#_of_Ratings',
                                                  'Budget',
                                                  'Opening_Weekend',
                                                  'Domestic_Gross',
                                                  'Worldwide_Gross'
                                                 ])
#     # Time milestone - Filmography processing done
#     print('Total time:')
#     print(pd.Timestamp.now() - filmostart)
    return filmspd
