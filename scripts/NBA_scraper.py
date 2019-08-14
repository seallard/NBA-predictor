import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from datetime import datetime

raw_file_path = "../data sets/raw_2018_19.csv"
season = "2019"

team_tags = ['ATL', 'BKN', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM',
             'MIA', 'MIL', 'MIN', 'NO', 'NYK', 'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'TOR', 'UTAH', 'WSH']

session = requests.session()

try:
    df = pd.read_csv(raw_file_path, error_bad_lines=False)
    old_game_ids = set(df['game_id'].tolist())
    old_game_ids_exist = True

except FileNotFoundError:
    old_game_ids = []
    old_game_ids_exist = False


def parse_html(url):
    html = session.get(url).text
    parsed_html = BeautifulSoup(html, "lxml")
    return parsed_html


def get_team_schedule(team_tag):
    html = parse_html('http://www.espn.com/nba/team/schedule/_/name/' + team_tag + '/season/' + season + '/seasontype/2')
    team_game_schedule = html.findChildren('table')[0]
    return team_game_schedule


def get_new_game_ids(team_game_schedule):

    new_game_ids = []

    for game in team_game_schedule.find_all("span", {"class": "ml4"}):
        game_link = game.find_all('a')[0]
        game_id = game_link['href'].split('=')[-1]

        if game_id not in new_game_ids and int(game_id) not in old_game_ids:
            new_game_ids.append(game_id)
            
    return new_game_ids


def get_game_date(game_html):
    date_string = game_html.title.string.split('-')[-2].replace(",", "").strip()
    formatted_date = datetime.strptime(date_string, '%B %d %Y').date()

    return formatted_date


def get_team_names(game_html):

    for div in game_html.find_all('div', class_='team away'):
        away_team = div.find('span', class_='short-name').text

    for div in game_html.find_all('div', class_='team home'):
        home_team = div.find('span', class_='short-name').text

    return away_team, home_team


def get_highlight_rows(game_html):
    table_rows = game_html.find_all('tr', class_='highlight')

    if len(table_rows) < 2: # Filter unplayed games.
        return None, None
    
    away_highlight = table_rows[0:2]
    home_highlight = table_rows[2:4]

    return away_highlight, home_highlight


def extract_box_score(highlight_rows):
    box_scores = []

    for highlight_row in highlight_rows:
        for score in highlight_row.find_all('td')[1:]:
            box_score = score.text

            if len(box_score) > 0:  # Ignore empty fields.
                if '%' in box_score:
                    box_score = box_score[:-1]

                box_scores.append(box_score)
                
    return box_scores


if __name__ == "__main__":

    with open(raw_file_path, 'a', newline='') as f:
        filewriter = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)

        if not old_game_ids_exist:
            filewriter.writerow(['fg', '3pt', 'ft', 'oreb', 'dreb', 'reb', 'ast', 'stl', 'blk', 'to', 
                                 'pf', 'pts', 'team', 'home', 'date', 'game_id', 'fg%', '3pt%', 'ft%'])

        for team_tag in team_tags:
            print(team_tag)
            team_game_schedule = get_team_schedule(team_tag)
            new_game_ids = get_new_game_ids(team_game_schedule)

            for game_id in new_game_ids:
                game_html = parse_html('http://www.espn.com/nba/boxscore?gameId=' + game_id)

                away_highlight, home_highlight = get_highlight_rows(game_html)

                if away_highlight is None:
                    break

                away_boxscore = extract_box_score(away_highlight)
                home_boxscore = extract_box_score(home_highlight)

                date = get_game_date(game_html)
                away_team, home_team = get_team_names(game_html)
                away_boxscore.extend([away_team, 0, date, game_id])
                home_boxscore.extend([home_team, 1, date, game_id])

                filewriter.writerow(away_boxscore)
                filewriter.writerow(home_boxscore)