import requests
from bs4 import BeautifulSoup

def soupify(url):
    "Takes a url and returns document."
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html5lib") 
    return soup
    
#Collect team name abbreviations.
soup = soupify('http://www.espn.com/nba/teams')
teams = []

for ul_tag in soup.find_all('ul', {'class': 'medium-logos'}):
    for li_tag in ul_tag.find_all('li'):
        teams.append(li_tag.a.get('href').split('/')[7]) #Extract abbreviations.