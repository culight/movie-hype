from bs4 import BeautifulSoup
import requests
import csv
import os
import database as db

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
def get_movie_urls(years):
    movie_thumbnails = []
    movie_urls = []

    for year in years:
        mov_list = get_movielist_url(year)
        list_html = get_html(mov_list)
        list_soup = BeautifulSoup(list_html, 'html.parser')
        movie_thumbnails = [t for t in list_soup.find_all('div', {'class':'thumbnail'})]
        for movie_thumbnail in movie_thumbnails:
            for movie in movie_thumbnail.children:
                if movie.name == 'a':
                    movie_urls.append(str(movie['href']))
    return movie_urls

# scrape the relevant data and store in a SQL database
def scrape(movie_urls, connection):
    movie_data = []
    print('scraping data from movie website...')

    get_names = "SELECT name FROM 'movie'"
    names = db.run_query(get_names, connection).fetchall()
    names = [n[0] for n in names]

    for url in movie_urls:
        data = {}
        movie_html = get_html(url)
        movie_soup = BeautifulSoup(movie_html, 'html.parser')

        title = get_title(movie_soup)
        if title not in names:
            print(title)
            continue

        data['name'] = title
        data['interest'] = get_interest(movie_soup)
        data['rating'] = get_rating(movie_soup)
        data['review_count'] = get_count(movie_soup)
        movie_data.append(data)
    print('done!')
    return movie_data

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

    if interest['wont see'] <= 0:
        interest['wont see'] = 1

    interest_score = float(interest['will see'])/float(interest['wont see'])

    return round(interest_score, 2)

def get_rating(movie_soup):
    r_num = movie_soup.find('strong', {'itemprop':'ratingValue'}).string
    rating = float(r_num)/5.0
    return round(rating, 2)

def get_count(movie_soup):
    count = movie_soup.find('strong', {'itemprop':'reviewCount'}).string
    return count

def get_news(movie_soup):
    pass

def convert_to_csv(data, file_path, file_name):
    if not data or len(data) < 1:
        print('no data available')

    print("creating ", file_name, "...")

    # delete the file if it exists (will rewrite)
    if os.path.exists(file_path + file_name):
        print('     rewriting...')
        os.remove(file_path + file_name)

    csv_filepath = os.path.join(file_path, file_name)

    with open(csv_filepath, 'w') as f:
        writer = csv.DictWriter(f,['name','interest', 'rating', 'review_count'])
        writer.writeheader()
        for datum in data:
            writer.writerow(datum)
    print('done!')
