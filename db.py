# db.py
# Author: Vanessa Lor
# Date: 5/15/2024

import sqlite3
from business import Player

def create_table():
    """Create a table for storing bowling scores in an SQLite database."""
    conn = sqlite3.connect('bowling_scores.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scores
                 (id INTEGER PRIMARY KEY,
                 first_name TEXT,
                 last_name TEXT,
                 score1 INTEGER,
                 score2 INTEGER,
                 score3 INTEGER,
                 score4 INTEGER,
                 avg_score REAL)''')
    conn.commit()
    conn.close()

def insert_player(first_name, last_name):
    """Insert a new player into the database."""
    conn = sqlite3.connect('bowling_scores.db')
    c = conn.cursor()
    c.execute('''INSERT INTO scores (first_name, last_name) VALUES (?, ?)''', (first_name, last_name))
    conn.commit()
    conn.close()

def update_score(player_id, column, new_score):
    """Update the score of a player in the database."""
    conn = sqlite3.connect('bowling_scores.db')
    c = conn.cursor()
    c.execute(f'''UPDATE scores SET {column} = ? WHERE id = ?''', (new_score, player_id))
    conn.commit()
    conn.close()

def delete_player(player_id):
    """Delete a player from the database."""
    conn = sqlite3.connect('bowling_scores.db')
    c = conn.cursor()
    c.execute('''DELETE FROM scores WHERE id = ?''', (player_id,))
    conn.commit()
    conn.close()
