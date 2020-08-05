# IMDB_film_data.py
# Ref. Development - IMDB Film Details Jupyter Notebook for more details
# Input: imdb_film_data(href_film)
# Output: filmdata
# Where filmdata is an array with href_film, title, year, imdb_rating, imdb_qty, budget, gross_wknd, gross_domestic, gross_ww

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from usd_conversion import usd_conversion

def imdb_film_data(href_film):
    # Append film_href input to full IMDB URL
    url = 'https://www.imdb.com' + href_film
    
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
        imdb_qty = float(str_imdb_qty)

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
    # Create variables gross_wknd, gross_domestic, gross_ww
    gross_wkndTag = soup.find('h4', text = re.compile('^Opening Weekend'))
    if gross_wkndTag is None:
        gross_wknd = None
        pass
    else:
        str_gross_wknd = gross_wkndTag.next_sibling
        gross_wknd = usd_conversion(str_gross_wknd)
    
    gross_domesticTag = soup.find('h4', text = re.compile('^Gross '))
    if gross_domesticTag is None:
        gross_domestic = None
        pass
    else:
        str_gross_domestic = gross_domesticTag.next_sibling
        gross_domestic = usd_conversion(str_gross_domestic)
    
    gross_wwTag = soup.find('h4', text = re.compile('^Cumulative Worldwide Gross'))
    if gross_wwTag is None:
        gross_ww = None
        pass
    else:
        str_gross_ww = gross_wwTag.next_sibling
        gross_ww = usd_conversion(str_gross_ww)

    # Return list of film data in prescribed order
    filmdata = [href_film, title, year, imdb_rating, imdb_qty, budget, gross_wknd, gross_domestic, gross_ww]
    return filmdata