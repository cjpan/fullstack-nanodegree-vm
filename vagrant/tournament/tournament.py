#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()

    c.execute("DELETE FROM matches;")
    DB.commit()

    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()

    c.execute("DELETE FROM players;")
    DB.commit()

    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()

    c.execute("SELECT COUNT(*) FROM players;")
    result = c.fetchone()[0]

    DB.close()

    return result


def registerPlayer(name):
    """Adds a player to the tournament database.

        The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    DB = connect()
    c = DB.cursor()

    # For SQL injection protection, use parameters.
    c.execute("INSERT INTO players (name) VALUES (%s);", (name, ))
    DB.commit()

    DB.close()


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

    DB = connect()
    c = DB.cursor()

    # Get the information from the created view.
    # Refer to tournamant.sql file for the view schema.
    c.execute("SELECT id, name, wins, total_matches FROM playerStandings;")
    result = c.fetchall()

    DB.close()

    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    DB = connect()
    c = DB.cursor()

    # For SQL injection protection, use parameters.
    c.execute("INSERT INTO matches (winner_id, loser_id) VALUES (%s, %s);",
              (winner, loser))
    DB.commit()

    DB.close()


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
    result = None

    DB = connect()
    c = DB.cursor()

    # Query for players number first
    c.execute('''SELECT COUNT(*) FROM players''')
    player_num = c.fetchone()[0]

    # Each 2 players become pair.
    # Each time, select 2 players with highest standings for next match.
    for i in range(0, player_num, 2):
        c.execute('''SELECT id, name, wins, total_matches FROM playerStandings
            LIMIT 2 OFFSET ''' + str(i) + ';')

        query_result = c.fetchall()

        # create the tuple for return value
        if result is not None:
            result = result, (query_result[0][0], query_result[0][1],
                              query_result[1][0], query_result[1][1])
        else:
            result = (query_result[0][0], query_result[0][1],
                      query_result[1][0], query_result[1][1])

    DB.close()

    return result
