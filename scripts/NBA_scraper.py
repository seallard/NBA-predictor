import requests
from bs4 import BeautifulSoup
import csv
import time
import pandas as pd
from datetime import datetime

# Load game id:s scraped previously (to reduce number of requests).
try:
    df = pd.read_csv("../data sets/2018_19_dataset.csv", error_bad_lines=False)
    previous_ids = set(df['id'].tolist())
    previous = True
    
except FileNotFoundError:
    previous_ids = []
    previous = False

def soupify(url):
    "Takes url and returns document."
    r = s.get(url)
    soup = BeautifulSoup(r.text,"html5lib") 
    time.sleep(1)
    return soup

team_tags = ['ATL', 'BKN', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET'	, 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 
             'MIA', 'MIL', 'MIN', 'NO', 'NYK', 'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'TOR', 'UTAH', 'WSH']

s = requests.session()

# Collect game id:s for each team. 
game_ids = []

for name in team_tags:
    print(name)
    soup = soupify('http://www.espn.com/nba/team/schedule/_/name/' + name + '/season/2019/seasontype/2')
    
    table = soup.findChildren('table')[0]

    for span in table.find_all("span", {"class": "ml4"}):
        links = span.find_all('a')
        
        for link in links:
            game_id = link['href'].split('=')[-1]
            
            if game_id not in game_ids and int(game_id) not in previous_ids:
                game_ids.append(game_id)
                       
# Collect box scores and team names for each collected game id and write to csv.
with open("../data sets/2018_19_dataset.csv", 'a', newline='') as f:
    filewriter = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)

    if not previous:
        filewriter.writerow(['fg','3pt','ft','oreb','dreb','reb','ast','stl','blk','to','pf','pts','id','team','home','date'])

    for i, game in enumerate(game_ids):
        print(game)

        soup = soupify('http://www.espn.com/nba/boxscore?gameId=' + game)
        
        # Get date for game. 
        date_string = soup.title.string.split('-')[-2].replace(",","").strip()
        formatted_date = datetime.strptime(date_string,'%B %d %Y').date()

        # Collect team names and home/away status for current game.
        teams = []
        for div in soup.find_all('div', class_='team away'):

            # Save team and home or away status in tuple (name, away=0)
            teams.append((div.find('span', class_='short-name').text, 0)) 
        
        for div in soup.find_all('div', class_='team home'):
            
             # Save team and home or away status in tuple (name, home=1)
            teams.append((div.find('span', class_='short-name').text, 1))

        # Collect box scores for current game.
        data = soup.find_all('tr', class_='highlight')

        # Select correct tables. 
        if len(data) > 2:

            # Extract relevant highlights.
            highlights = [data[0], data[2]]
            
            for k, scores in enumerate(highlights):
                team_data = []

                for td_tag in scores.find_all('td'):
                    
                    # Ignore empty fields.
                    if len(td_tag.text) > 0: 
                        team_data.append(td_tag.text)

                team_data.extend((game, teams[k][0],teams[k][1],formatted_date))
                filewriter.writerow(team_data[1:])