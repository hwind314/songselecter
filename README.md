# Song Searcher
#### Video Demo:  <URL HERE>
#### Description:
Summary
    Search for songs in 3 different ways: random song generator, search based on mood with a quiz, specific search.
    See how many of each search you make and history of search results

dataset.csv
    Kaggle datasource: https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset?resource=download
    data used for this project from Spotify with 21 columns. Song recommendation will be from this list.

datatransfer.py
    creating a data.db using dataset.csv

data.db
    songs: data transferred from dataset.csv
    users: table to keep track of user information
    sqlite_sequence: generate user id by incrementing 1
    history: results generated from search.html
    search: counter for the different searches

'''
    CREATE TABLE IF NOT EXISTS "songs" (
    "Unnamed: 0" INTEGER,
    "track_id" TEXT,
    "artists" TEXT,
    "album_name" TEXT,
    "track_name" TEXT,
    "popularity" INTEGER,
    "duration_ms" INTEGER,
    "explicit" INTEGER,
    "danceability" REAL,
    "energy" REAL,
    "key" INTEGER,
    "loudness" REAL,
    "mode" INTEGER,
    "speechiness" REAL,
    "acousticness" REAL,
    "instrumentalness" REAL,
    "liveness" REAL,
    "valence" REAL,
    "tempo" REAL,
    "time_signature" INTEGER,
    "track_genre" TEXT
    );
    CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
    );
    CREATE TABLE sqlite_sequence(name,seq);
    CREATE TABLE history (
        id INTEGER,
        track_id TEXT,
        search_id INTEGER,
        FOREIGN KEY (id) REFERENCES users(id)
    );
    CREATE TABLE search (
    id INTEGER,
    luck INTEGER
    , find INTEGER,
    search INTEGER,
    FOREIGN KEY (id) REFERENCES users(id));
'''

app.py
    file where all functions needed for website is stored

styles.css
    css file for appearance of website. theme from: https://bootswatch.com/quartz/

layout.html
    navigation bar that is located on every page

index.html
    will redirect to login.html if not logged in. otherwise shows homepage with search button and search counter

register.html
    if user doesn't have account, then they need to register first with a valid email and password and confirmation need the same input

login.html
    login if already registered. need to match registered details

searcher.html
    main search webpage, navigation bar links to this page. 3 buttons for different types of searches.
    3 search choices were selected to give users a range of options to choose from.

lucky.html
    randomly selects one songs from songs table

search.html
    form for users to fill out with sliding scale and submit button

searched.html
    results from search.html. if no identical match found, then top 10 matches will be shown

find.html
    users can search for specific song, artist or album in text field and dropdown menu

found.html
    result from find.html. shows results that contain text within selected field

history.html
    view search results from searched.html.
    doesn't show results from find.html as some have a lot of results that are irrelevant for users.
    doesn't show results from lucky.html as users didn't specifically look for these songs.

apology.html
    anything that goes wrong will redirect to this page. e.g. you didn't enter a password when registering

