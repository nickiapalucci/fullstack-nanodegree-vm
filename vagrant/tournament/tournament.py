#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Reset match count to 0 in table players in database tournament"""
    conn = connect()
    c = conn.cursor()
    c.execute("UPDATE players SET matches = 0;")
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all data from table players"""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM players;")
    conn.commit()
    conn.close()

def countPlayers():
    """Count all rows in table players, return integer of result"""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT (*) FROM players;")
    player_count = c.fetchone()
    conn.close()
    return int(player_count[0])

def registerPlayer(name):
    """Add a player to the database"""
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO players (name) VALUES (%s);", (name,))
    conn.commit()
    conn.close()

def playerStandings():
    """Sort all rows in database by column wins.  Return
       a list of tuples with (id, name, wins, matches)"""
    conn = connect()
    c = conn.cursor()
#   create a list of tuples
    c.execute("SELECT * FROM players ORDER BY wins;")
    standings = c.fetchall()
    c = conn.close()
    return standings

def reportMatch(winner, loser):
    """Record the outcome of a single match between two players"""
    conn = connect()
    c = conn.cursor()
#   Update Match Count of both players
    c.execute("""UPDATE players SET matches = matches + 1
               WHERE player_id = %s;""", (winner,))
    c.execute("""UPDATE players SET matches = matches + 1
               WHERE player_id = %s;""", (loser,))
#   Update Win Count of winner
    c.execute("""UPDATE players SET wins = wins + 1
              WHERE player_id = %s;""", (winner,))
    conn.commit()
    conn.close()
 
def swissPairings():
    """Sort rows by wins
       Create an output of player's id and name
       Create a list of tuples with (id1, name1, id2, name2)"""
    conn = connect()
    c = conn.cursor()
#   Create list of tuples from database
    c.execute("SELECT player_id, name FROM players ORDER BY wins DESC;")
    pairings = c.fetchall()
    conn.close()
#   Unpack tuples and create new list of matched pairs
    swiss_pairing = []
    for x in pairings:
        if len(pairings) >= 2:
            (pid1, pname1) = pairings.pop(0)
            (pid2, pname2) = pairings.pop(0)
            a = (pid1, pname1, pid2, pname2)
            swiss_pairing.append(a)
        elif len(pairings) == 1:
#   future feature, odd player wins bye once only
            break
        else:
            break
    return swiss_pairing

