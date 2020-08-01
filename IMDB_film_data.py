# IMDB_film_data.py
# Ref. Development - IMDB Film Details Jupyter Notebook for more details

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from usd_conversion import usd_conversion

def imdb_film_data(href_film):
    # Append href_film input to full IMDB URL
    url = 'https://wwwimdb.com' + href_film
    
    # Parse IMDB URL with BeautifulSoup
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    # Retrieve film title and release year data
    # Create variables title, year
    imdbFilmdata = soup.find('div', class_ = 'title_wrapper')
    title_year = imdbFilmdata.h1.text
    if imdbFilmdata.h1.span is None:
        title_year = title_year.replace(u'\xa0',u' ')
        title = title_year.strip()
        year = None
        pass
    else:
        yearbrackets = imdbFilmdata.h1.span.text
        title = title_year[:-len(yearbrackets)-2]
        yearstr = yearbrackets[1:len(yearbrackets)-1]
        year = int(yearstr)
    
    # Retrieve IMDB Rating and number of ratings submitted data
    # Create variables imdb_rating, imdb_qty
    imdbRatingdata = soup.find('div', class_ = 'imdbRating')
    if imdbRatingdata is None:
        imdb_rating = None
        imdb_qty = None
        pass
    else:
        str_imdb_rating = imdbRatingdata.strong.text
        str_imdb_qty = imdbRatingdata.a.text
        imdb_rating = float(str_imdb_rating)
        str_imdb_qty = str_imdb_qty.replace(',','')
        imdb_qty = int(str_imdb_qty)

    # Retrieve budget data
    # Create variable budget
    budgetTag = soup.find('h4', text = re.compile('^Budg'))
    if budgetTag is None:
        budget = None
        pass
    else:
        str_budget = budgetTag.next_sibling
        budget = usd_conversion(str_budget)

    # Retrieve box office data including opening weekend, gross domestic, and worldwide gross values
    # Create variable opening_wknd, gross_domestic, ww_gross
    openingTag = soup.find('h4', text = re.compile('^Opening Weekend'))
    if openingTag is None:
        opening_wknd = None
        pass
    else:
        str_opening_wknd = openingTag.next_sibling
        opening_wknd = usd_conversion(str_opening_wknd)
    
    domesticTag = soup.find('h4', text = re.compile('^Gross '))
    if domesticTag is None:
        gross_domestic = None
        pass
    else:
        str_gross_domestic = domesticTag.next_sibling
        gross_domestic = usd_conversion(str_gross_domestic)
    
    worldwideTag = soup.find('h4', text = re.compile('^Cumulative Worldwide Gross'))
    if worldwideTag is None:
        ww_gross = None
        pass
    else:
        str_ww_gross = worldwideTag.next_sibling
        ww_gross = usd_conversion(str_ww_gross)

    # Return list of film data in prescribed order
    filmdata = [href_film, title, year, imdb_rating, imdb_qty, budget, opening_wknd, gross_domestic, ww_gross]
    return filmdata