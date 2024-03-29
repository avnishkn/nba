import requests
import mysql.connector

headers = {
    'x-rapidapi-host': 'api-nba-v1.p.rapidapi.com',
    'x-rapidapi-key': # Insert RapidAPI key
}

cnx = mysql.connector.connect(
    host='localhost',
    user='root',
    password= # Insert password,
    database='nba_database'
)
cursor = cnx.cursor()

# Create tables for teams and players
cursor.execute('''
CREATE TABLE IF NOT EXISTS teams (
    team_id INT PRIMARY KEY,
    team_name VARCHAR(255)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS players (
    player_name VARCHAR(255),
    team_id INT,
    FOREIGN KEY(team_id) REFERENCES teams(team_id)
)
''')

# Fetch all NBA teams and players to populate tables
teams_response = requests.get('https://api-nba-v1.p.rapidapi.com/teams', headers=headers)
teams_data = teams_response.json()
team_values = [(team['id'], team['name']) for team in teams_data['response']]
insert_teams_data = 'INSERT IGNORE INTO teams (team_id, team_name) VALUES (%s, %s)'
cursor.executemany(insert_teams_data, team_values)
cnx.commit()

for team in teams_data['response'][:30]:
    team_id = team
    querystring = {"team":team_id,"season":"2022"}

    try:
        players_response = requests.get('https://api-nba-v1.p.rapidapi.com/players', headers=headers, params=querystring)
        players_data = players_response.json()

        if 'response' not in players_data:
            print(f"No 'response' key for team id: {team_id}")
            continue

        player_values = [(player['firstname'] + ' ' + player['lastname'], team_id) for player in players_data['response']]
        insert_players_data = 'INSERT IGNORE INTO players (player_name, team_id) VALUES (%s, %s)'
        cursor.executemany(insert_players_data, player_values)
        cnx.commit()

    except Exception as e:
        print(f"Error with team id {team_id}: {e}")

# Close the database connection
cursor.close()
cnx.close()
