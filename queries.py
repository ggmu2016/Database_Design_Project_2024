from query_to_table import Query2TupleLarge
import time
from libra import libra

queries = [
    "SELECT * FROM teams;",
    "SELECT \"teamName\" FROM teams;",
    "SELECT \"teamName\" FROM teams WHERE city='Brandonport';",
    "SELECT DISTINCT players.\"playerName\" FROM players WHERE position='Goalkeeper';",
    "SELECT DISTINCT \"teamName\" FROM teams JOIN merchandise ON teams.\"teamID\" = merchandise.\"teamID\" WHERE price>70;",
    "SELECT teams.\"teamName\", players.\"playerName\" FROM teams JOIN players on teams.\"teamID\"=players.\"teamID\";",
    "SELECT players.\"playerName\", teams.\"teamName\" FROM players JOIN teams ON players.\"teamID\" = teams.\"teamID\" WHERE teams.city = 'Brandonport';",
    "SELECT players.\"playerName\" FROM players JOIN teams ON players.\"teamID\" = teams.\"teamID\" WHERE age<26 and \"teamName\"='Prince Group';",
    "SELECT DISTINCT teams.\"teamName\" FROM players JOIN teams ON players.\"teamID\" = teams.\"teamID\" WHERE age>33;",
    # "SELECT DISTINCT players.\"playerName\", teams.\"teamName\" FROM players JOIN teams ON players.\"teamID\" = teams.\"teamID\" WHERE position='Defender';",
    "SELECT DISTINCT teams.\"teamName\" FROM players JOIN teams ON players.\"teamID\" = teams.\"teamID\" JOIN merchandise ON teams.\"teamID\"=merchandise.\"teamID\" WHERE age>33 and price>70;",

    # "SELECT name FROM teams JOIN  matches on \"teamID\"=\"homeTeamID\" WHERE \"homeScore\" > 3;",
    # "SELECT name FROM teams JOIN  matches on \"teamID\"=\"homeTeamID\" WHERE \"homeScore\" > 3 and \"awayScore\" < 2;",
    # "SELECT name FROM teams JOIN  matches on \"teamID\"=\"homeTeamID\" WHERE \"homeScore\" > \"awayScore\";",
    # "SELECT player.name FROM teams JOIN  players JOIN matches on \"teamID\"=\"homeTeamID\" WHERE \"homeScore\" > \"awayScore\" and position='Forward';",
    # "SELECT home_team.name, away_team.name, matches.\"homeScore\", matches.\"awayScore\" FROM matches JOIN teams AS home_team ON matches.\"homeTeamID\" = home_team.\"teamID\" JOIN teams AS away_team ON matches.\"awayTeamID\" = away_team.\"teamID\" WHERE matches.\"homeScore\" > matches.\"awayScore\";"
]

def get_O_neg_query(query):
    if len(query.split("WHERE")) < 2:
        return None
    selection_str = query.split("WHERE")[0]
    selected_cols = selection_str.split("SELECT")[1].split("FROM")[0].replace(" DISTINCT", "")
    if len(selected_cols.split(",")):
        selected_cols = f' ({selected_cols.strip()}) '
    query = query.replace(";","")
    return f'{selection_str}WHERE{selected_cols}NOT IN ({query});' 

def time_queries():
    times = []
    for q in queries:
        O_pos = Query2TupleLarge(q)
        O_neg = Query2TupleLarge(get_O_neg_query(q)) if get_O_neg_query(q) else []
        start = time.time()
        libra(O_pos, O_neg)
        end = time.time()
        times.append(end - start)
    return times
