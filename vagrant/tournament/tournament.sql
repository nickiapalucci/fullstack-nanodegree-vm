-- Table definitions for the tournament project.
-- Run this before running tournament.py

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE players (
    player_id serial primary key,
    name text,
    wins int DEFAULT 0,
    matches int DEFAULT 0
);
