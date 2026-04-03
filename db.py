"""Database helper functions for SQLite3 with Flask context."""

import sqlite3
from flask import g


def get_connection():
    """Return a new SQLite connection with foreign keys enabled."""
    con = sqlite3.connect("database.db")
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con


def execute(sql, params=None):
    """Execute an SQL command with optional parameters and commit changes."""
    if params is None:
        params = []
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
    con.close()


def last_insert_id():
    """Return the last inserted row ID stored in Flask's g."""
    return g.last_insert_id


def query(sql, params=None):
    """Execute an SQL query with optional parameters and return all results."""
    if params is None:
        params = []
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result
