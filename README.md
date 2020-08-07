# IMDB-boxoffice-scraper
Project is a web scraper tool to collect box office data from IMDB.  Functions are hardcoded to pull specific fields but can be easily modified to adapt to different needs.

This project includes the following functions:
```
IMDB_film_data.py
IMDB_filmo_scraper.py
usd_conversion.py
```

## Getting Started
The IMDB_filmo_scraper takes an IMDB actor or actress href to extract basic data like the actor or actress's full name and date of birth, and to build a list of IMDB film href links to iterate the IMDB_film_data function.

### Example
For actor Tom Cruise, the full IMDB link is:
```
https://www.imdb.com/name/nm0000129/
```
To use the IMDB_filmo_scraper function, call the following:
```
imdb_filmo_scraper('/nm0000129/')
```

Within the IMDB_filmo_scraper function, it will call the IMDB_film_data function.  This function uses a film href.  For example, the full IMDB URL for Mission: Impossible 7 is:
```
https://www.imdb.com/title/tt9603212/
```
The IMDB_film_data function will iterate the following:
```
imdb_film_data('/tt9603212/')
```
## Development
For development details, please refer to the accompanying Jupyter Notebooks in the repository.
