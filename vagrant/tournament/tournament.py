#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    conn = connect()
    c = conn.cursor()
    c.execute("UPDATE players SET matches = 0;")
    conn.commit()
    conn.close()

def deletePlayers():
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM players;")
    conn.commit()
    conn.close()

def countPlayers():
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT (*) FROM players;")
    player_count = c.fetchone()
    conn.close()
    return int(player_count[0])

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO players (name) VALUES (%s);", (name,))
    conn.commit()
    conn.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM players ORDER BY wins;")
    standings = c.fetchall()
    c = conn.close()
    print standings
    return standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
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
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
#   Establish psycopg cursor
    conn = connect()
    c = conn.cursor()
#   Create list of tuples from database players
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
#           future feature, odd player wins bye once only
            break
        else:
            break
    print swiss_pairing
    return swiss_pairing

