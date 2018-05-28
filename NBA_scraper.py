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

#Collect all game id:s for each team. 
game_ids = []

for name in teams:
    soup = soupify('http://www.espn.com/nba/team/schedule/_/name/' + name + '/seasontype/2')

    for ul_tag in soup.find_all('ul', {'class': 'game-schedule'}):
        for li_tag in ul_tag.find_all('li',{'class': 'score'}):
            game = li_tag.a.get('href')[30:39] #Extract id number.
            if game not in game_ids: #Avoid duplicates.
                game_ids.append((game, name))