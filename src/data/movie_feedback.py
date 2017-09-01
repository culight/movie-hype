import os
from bs4 import BeautifulSoup
import requests

BASE_URL = 'https://www.movieinsider.com/movies/popular/'
PAGE_OFFSET = '?page_offset='

# build url for popular movies for a particular year as specified by endpoint
def get_movielist_url(endpoint, offset=0):
    return BASE_URL + endpoint + PAGE_OFFSET + str(offset)

# get html for a particular movie from the movies array
def get_html(url):
    request = None
    request = requests.get(url)
    if request.ok:
        return request.text
    else:
        print(request.status_code)

# form a list of movie urls
def get_movie_urls(list_html):
    movie_thumbnails = []
    movie_urls = []

    list_soup = BeautifulSoup(list_html, 'html.parser')
    movie_thumbnails = [t for t in list_soup.find_all('div', {'class':'thumbnail'})]
    for movie_thumbnail in movie_thumbnails:
        for movie in movie_thumbnail.children:
            if movie.name == 'a':
                movie_urls.append(str(movie['href']))
    return movie_urls

# scrape the relevant data and store in a SQL database
def scrape(movie_urls):
    for url in movie_urls:
        movie_data = {}
        movie_html = get_html(url)
        movie_soup = BeautifulSoup(movie_html, 'html.parser')

        title = get_title(movie_soup)
        if not is_movie_present(title):
            continue

        movie_data['title'] = title
        movie_data['interest score'] = get_interest(movie_soup)
        print(movie_data)
        # title
        # cross_check title
        # get will see/wont see dictionary
        # ratings

# get the title of the movie
def get_title(movie_soup):
    title = movie_soup.find('title').string
    return title[0:-13]

# get the see/won't see numbers for a particular movie url
def get_interest(movie_soup):
    interest = {}

    will_see = movie_soup.find('button', {'class':'btn-success'})
    wont_see = movie_soup.find('button', {'class':'btn-danger'})

    for child in will_see.children:
        if child.name == 'span' and 'seeCount' in child['id']:
            interest['will see'] = int(child.string.replace(',',''))

    for child in wont_see.children:
        if child.name == 'span' and 'seeCount' in child['id']:
            interest['wont see'] = int(child.string.replace(',',''))

    interest_score = float(interest['will see'])/float(interest['wont see'])

    return round(interest_score, 2)



# use the title to check if this movie is present in the other dataset
def is_movie_present(title):
    return True
