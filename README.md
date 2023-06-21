## NBA
This project uses an API to pull data on current NBA players and their most recent teams.
* Data is stored in 2 tables in a SQL database
* These are linked using the team ID as a foreign key in the players' table

The teams table provides a mapping of team_id to team_name - with this we can run a query to pull all current Miami Heat players
```
SELECT players.player_name, teams.team_name FROM players
JOIN teams ON players.team_id = teams.team_id
WHERE teams.team_name = 'Miami Heat'
```
