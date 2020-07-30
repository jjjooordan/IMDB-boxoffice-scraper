# IMDB_film_data.py
# Ref. Development - IMDB Film Details Jupyter Notebook for more details

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from usd_conversion import usd_conversion

def imdb_film_data(film_href):
    # Append film_href input to full IMDB URL
    url = 'https://www.imdb.com' + film_href
    
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
    # Create variables imdbRating, imdbRatingQty
    imdbRatingdata = soup.find('div', class_ = 'imdbRating')
    if imdbRatingdata is None:
        imdbRating = None
        imdbRatingQty = None
        pass
    else:
        str_imdbRating = imdbRatingdata.strong.text
        str_imdbRatingQty = imdbRatingdata.a.text
        imdbRating = float(str_imdbRating)
        str_imdbRatingQty = str_imdbRatingQty.replace(',','')
        imdbRatingQty = int(str_imdbRatingQty)

    # Retrieve budget data
    # Create variable budgetVal
    budgetTag = soup.find('h4', text = re.compile('^Budg'))
    if budgetTag is None:
        budgetVal = None
        pass
    else:
        str_budgetVal = budgetTag.next_sibling
        budgetVal = usd_conversion(str_budgetVal)

    # Retrieve box office data including opening weekend, gross domestic, and worldwide gross values
    # Create variable openingVal, domesticVal, worldwideVal
    openingTag = soup.find('h4', text = re.compile('^Opening Weekend'))
    if openingTag is None:
        openingVal = None
        pass
    else:
        str_openingVal = openingTag.next_sibling
        openingVal = usd_conversion(str_openingVal)
    
    domesticTag = soup.find('h4', text = re.compile('^Gross '))
    if domesticTag is None:
        domesticVal = None
        pass
    else:
        str_domesticVal = domesticTag.next_sibling
        domesticVal = usd_conversion(str_domesticVal)
    
    worldwideTag = soup.find('h4', text = re.compile('^Cumulative Worldwide Gross'))
    if worldwideTag is None:
        worldwideVal = None
        pass
    else:
        str_worldwideVal = worldwideTag.next_sibling
        worldwideVal = usd_conversion(str_worldwideVal)

    # Return list of film data in prescribed order
    filmdata = [film_href, title, year, imdbRating, imdbRatingQty, budgetVal, openingVal, domesticVal, worldwideVal]
    return filmdata