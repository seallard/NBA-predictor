import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

s = requests.session()

def soupify(url):
    "Takes url and returns document."
    r = s.get(url)
    soup = BeautifulSoup(r.text,"html5lib") 
    return soup

# Team name abbreviations.
team_tags = ['ATL', 'BKN', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET'	, 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 
             'MIA', 'MIL', 'MIN', 'NO', 'NYK', 'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'TOR', 'UTAH', 'WSH']

# Collect game id:s and dates for each team and game. 
game_ids = []
dates = []

for name in team_tags:
    print(name)
    soup = soupify('http://www.espn.com/nba/team/schedule/_/name/' + name + '/season/2019/seasontype/2')
    
    # Find table containing games. 
    table = soup.findChildren('table')[0]

    for span in table.find_all("span", {"class": "ml4"}):
        links = span.find_all('a')
        
        for link in links:
            game_id = link['href'].split('=')[-1]
            
            if game_id not in game_ids:
                game_ids.append(game_id)

    # Iterate over table rows. 
    for row in  table.findChildren('tr'):
        for data in row.findChildren('td'):
            
            if ',' in data.text and 'tickets' not in data.text:

                if any(m in data.text for m in ['Oct','Nov','Dec']):
                    year = '2018'

                else:
                    year = '2019'
                
                # Convert date string to date object.
                formatted_date = datetime.strptime(year + data.text.split(',')[-1],'%Y %b %d').date()

                # Save if game has been played.
                if formatted_date < datetime.now().date():
                    dates.append(formatted_date)
print(len(game_ids))
# Collect box scores and team names for each collected game id and write to csv.
with open('NBA_game_stats.csv','w', newline='') as csvfile:

    filewriter = csv.writer(csvfile, delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['fg','3pt','ft','oreb','dreb','reb','ast','stl','blk','to','pf','pts','id','team','home','date'])
    
    # Iterate over game id:s and collect game statistics.
    for i, game in enumerate(game_ids):
        soup = soupify('http://www.espn.com/nba/boxscore?gameId=' + game)
        
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

        # Game id:s for unplayed games have been collected. Check that data exist for current game.
        if len(data) > 2:

            # Extract relevant highlights.
            highlights = [data[0], data[2]]
            
            for k, scores in enumerate(highlights):
                team_data = []

                for td_tag in scores.find_all('td'):
                    
                    # Ignore empty fields.
                    if len(td_tag.text) > 0: 
                        team_data.append(td_tag.text)

                team_data.extend((game, teams[k][0],teams[k][1], dates[i]))
                filewriter.writerow(team_data[1:])