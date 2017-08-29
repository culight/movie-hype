import os
from bs4 import BeautifulSoup
import requests

base_url = 'https://www.movieinsider.com/movies'

def get_url(endpoint='/popular'):
    return base_url + endpoint

def get_html(url):
    request = None
    request = requests.get(url)
    if request.ok:
        return request.text
    else:
        print(request.status_code)

def scrape_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    pass
