import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def soupify(url):
    "Takes url and returns document."
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html5lib") 
    return soup

#Collect team name abbreviations.
soup = soupify('http://www.espn.com/nba/teams')
teams = []

for ul_tag in soup.find_all('ul', {'class': 'medium-logos'}):
    for li_tag in ul_tag.find_all('li'):
        teams.append(li_tag.a.get('href').split('/')[7]) #Extract abbreviations.

#Collect all game id:s and dates for each team. 
game_ids = []
dates = []
months = ['Oct','Nov','Dec']

for name in teams:
    soup = soupify('http://www.espn.com/nba/team/schedule/_/name/' + name + '/seasontype/2')

    #Collecting dates.
    data = soup.find_all('div',{'class':'mod-content'})

    for date in data[0].find_all('td'):
        if ',' in date.text: #Only date td contain ','.
            if any(m in date.text for m in months):
                year = '2017'
            else:
                year = '2018'
            
            formatted_date = datetime.strptime(year + date.text.split(',')[-1],'%Y %b %d').date()
            dates.append(formatted_date)

    #Collecting id:s.
    for ul_tag in soup.find_all('ul', {'class': 'game-schedule'}):
        for li_tag in ul_tag.find_all('li',{'class': 'score'}):
            game = li_tag.a.get('href')[30:39] #Extract id number.

            if game not in game_ids: #Avoid duplicates.
                game_ids.append(game)

#Collect box scores for each collected game id and write to csv.
with open('NBA_game_stats.csv','w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['fg','3pt','ft','oreb','dreb','reb','ast','stl','blk','to','pf','pts','id','team','date'])
    
    for i,game in enumerate(game_ids):
        soup = soupify('http://www.espn.com/nba/boxscore?gameId=' + game)
        data = soup.find_all('tr',{'class': 'highlight'})

        highlights = [data[0],data[2]] #Extract relevant highlights.

        for scores in highlights:
            team_data= []

            for td_tag in scores.find_all('td'):
                if len(td_tag.text) > 0: #Ignore empty fields.
                    team_data.append(td_tag.text)
        
            team_data.append(game)
            team_data.append(dates[i])
            filewriter.writerow(team_data[1:])