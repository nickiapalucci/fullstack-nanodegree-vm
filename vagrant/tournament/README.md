## Synopsis

This project demonstrates the capabilities of an sql database being queried and modified by a program written in python by creating a "swiss tournament" style of creating pairs of players in a sports competition.

## Code Example
    c.execute("SELECT player_id, name FROM players ORDER BY wins DESC;")
    pairings = c.fetchall()
    swiss_pairing = []
    for x in pairings:
        if len(pairings) >= 2:
            (pid1, pname1) = pairings.pop(0)
            (pid2, pname2) = pairings.pop(0)
            a = (pid1, pname1, pid2, pname2)
            swiss_pairing.append(a)

## Motivation

This project was forked from a github repository created and maintained by udacity.com for students to build from as a requirement for a certification in full stack web development.

## Installation

This project can be run in a vagrant virtual machine configured by udacity.com.  The vagrant configuration file is located in repository provided by udacity.com

## API Reference

A copy of the psycopg2 python library is required and also included in the repository provided by udacity.com

## Tests

Begin by navigating to /vagrant/tournament/ and running tournament.sql from within psql.  This will create the database and tables and connect to them.  Then run tournament_test.py from the command line.  A successful run will display 8 printed lines of actions that were successfully accomplished, and no errors should occur.

