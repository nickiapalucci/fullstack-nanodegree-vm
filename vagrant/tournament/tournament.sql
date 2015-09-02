-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE players (
    player_id serial primary key,
    name text
);

CREATE TABLE matches (
    match_id serial primary key,
    winner integer references players(player_id),
    loser integer references players(player_id)
);

CREATE VIEW win_count AS
    SELECT player_id, name,
    COUNT (winner) AS wins
    FROM players
    LEFT OUTER JOIN
        matches ON players.player_id=matches.winner
    GROUP BY player_id
    ORDER BY player_id;

CREATE VIEW loss_count AS
    SELECT player_id, name,
    COUNT (loser) AS losses
    FROM players
    LEFT OUTER JOIN
        matches ON players.player_id=matches.loser
    GROUP BY player_id
    ORDER BY player_id;

CREATE VIEW total_count AS
    SELECT win_count.player_id,
    SUM(win_count.wins + loss_count.losses) as total
    FROM win_count JOIN loss_count 
        ON win_count.player_id = loss_count.player_id
    GROUP BY win_count.player_id
    ORDER BY win_count.player_id;
