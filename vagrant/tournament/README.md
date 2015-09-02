## Synopsis

Tournament.py contains functions for administering a gaming tournament that uses "swiss-style" pairings.  The functions in tournament.py are meant to be included in other programs ... it has no main() function.  Tournament_test.py will test these functions and print an 8 step list of actions ending with "Success!" or descriptive errors.  Tournament.sql

## Motivation

This project was forked from a github repository created and maintained by udacity.com for students to build from as a requirement for a certification in full stack web development.

## Installation

This project requires python with the psycopg2 library and psql.  There are three files that should be present within one folder: tournament.sql, tournament.py, tournament_test.py. Begin by running tournament.sql from the command line to establish the databases and views. If the tournament database has previously been created, it must be dropped manually.  See the Tests section below for testing the installation.

## API Reference

A copy of the psycopg2 python library is required and can be downloaded from http://initd.org/psycopg/download/

## Tests

Begin by navigating to /vagrant/tournament/ and running tournament.sql from within psql.  This will create the database and tables and connect to them.  Then run tournament_test.py from the command line.  A successful run will display 8 printed lines of actions that were successfully accomplished, and no errors should occur.


