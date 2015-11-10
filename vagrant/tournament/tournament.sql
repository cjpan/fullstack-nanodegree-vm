-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

CREATE TABLE players ( name TEXT,
                     id SERIAL primary key);

CREATE TABLE matches ( match_id SERIAL primary key,
                       winner_id INTEGER REFERENCES players,
                       loser_id INTEGER REFERENCES players);

-- Create view for player standings.
-- Wins is got from the player table left joining the matches table 
-- where the player id is the winning id;
-- Total matches is got from the player table left joining the matches table 
-- where the player id is winning id or loser id;
CREATE VIEW playerStandings AS 
    SELECT players.id, players.name, w.wins, tm.total_matches FROM players 
        LEFT JOIN (SELECT players.id, COUNT(winner_id) AS wins FROM players 
                       LEFT JOIN matches ON players.id = winner_id 
                       GROUP BY players.id) AS w ON players.id = w.id
        LEFT JOIN (SELECT players.id, COUNT(match_id) AS total_matches FROM players 
                       LEFT JOIN matches ON players.id = winner_id OR players.id = loser_id 
                       GROUP BY players.id) AS tm ON players.id = tm.id
        ORDER BY w.wins DESC;
