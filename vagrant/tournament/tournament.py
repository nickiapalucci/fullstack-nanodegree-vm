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
    c.execute("DELETE FROM matches;")
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
    c.execute("""SELECT 
                 win_count.player_id, 
                 win_count.name,
                 win_count.wins,
                 total_count.total
                 FROM win_count, loss_count, total_count
                 GROUP BY 
                     win_count.player_id,
                     win_count.name,
                     win_count.wins,
                     total_count.total
                 ORDER BY
                     wins DESC;""")
    standings = c.fetchall()
    return standings
    conn.close()


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    c.execute("""INSERT INTO matches (winner, loser)
                 VALUES (%s, %s);""", (winner, loser,))
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
    pairings = playerStandings()
    swiss_pairing = []
    for x in pairings:
        if len(pairings) >= 2:
            (pid1, pname1, c1, d1) = pairings.pop(0)
            (pid2, pname2, c2, d2) = pairings.pop(0)
            a = (pid1, pname1, pid2, pname2)
            swiss_pairing.append(a)
        elif len(pairings) == 1:  # For future use of odd number of players
            break
        else:
            break
    return swiss_pairing

