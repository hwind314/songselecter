import pandas as pd
import sqlite3

# Read CSV file into DataFrame
df = pd.read_csv('dataset.csv')

# Connect to SQLite database (or create it)
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Create table (adjust columns as needed)
cursor.execute('''CREATE TABLE songs (
               id INTEGER PRIMARY KEY,
               track_id TEXT, artists TEXT,
               album_name TEXT,
               track_name TEXT,
               popularity INTEGER,
               duration_ms INTEGER,
               explicit BOOLEAN,
               danceability REAL,
               energy REAL,
               key INTEGER,
               loudness REAL,
               mode INTEGER,
               speechiness REAL,
               acousticness REAL,
               instrumentalness REAL,
               liveness REAL,
               valence REAL,
               templo REAL,
               time_signature INTEGER,track_genre TEXT
               )''')

# Insert DataFrame data into the table
df.to_sql('songs', conn, if_exists='replace', index=False)

# Commit and close connection
conn.commit()
conn.close()
