import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask import redirect, render_template, request, session
from functools import wraps

# Configure application
app = Flask(__name__, static_folder='/workspaces/126040044/project/static')

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///data.db")

def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    userid = session["user_id"]
    luck_result = db.execute("SELECT luck FROM search WHERE id = ?", userid)
    find_result = db.execute("SELECT find FROM search WHERE id = ?", userid)
    search_result = db.execute("SELECT search FROM search WHERE id = ?", userid)

    print(userid)
    print(find_result)
    print(search_result)

    if luck_result and find_result and search_result:
        luck = luck_result[0]["luck"]
        find = find_result[0]["find"]
        search = search_result[0]["search"]
    else:
        luck = find = search = 0

    return render_template("index.html", luck=luck, find=find, search=search)

@app.route("/searcher", methods=["GET"])
@login_required
def searcher():
    return render_template("searcher.html")

@app.route("/lucky")
@login_required
def lucky():
    luck = db.execute("SELECT * FROM songs ORDER BY RANDOM() LIMIT 1")
    userid = session["user_id"]
    db.execute("UPDATE search SET luck = luck + 1 WHERE id = ?", userid)
    return render_template("lucky.html", luck=luck)

@app.route("/find", methods=["GET","POST"])
@login_required
def find():
    if request.method == "GET":
        return render_template("find.html")
    elif request.method == "POST":
        answer = request.form.get("answer")
        select = request.form.get("select")
        query = f"SELECT * FROM songs WHERE {select} LIKE ?"
        results = db.execute(query, f"%{answer}%")
        userid = session["user_id"]
        db.execute("UPDATE search SET find = find + 1 WHERE id = ?", userid)
        return render_template("found.html", answer=answer, select=select, results=results)
    else:
        return render_template("apology.html"), 400


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    if request.method == "GET":
        return render_template("search.html")
    elif request.method == "POST":
        danceability = request.form.get("danceability")
        energy = request.form.get("energy")
        speechiness = request.form.get("speechiness")
        valence = request.form.get("valence")
        user_id = session["user_id"]
        results = db.execute("SELECT DISTINCT * FROM songs WHERE danceability = ? AND energy = ? AND speechiness = ? AND valence = ?", danceability, energy, speechiness, valence)
        num_results = len(results)

        searchid_row = db.execute("SELECT MAX(search_id) AS max_search_id FROM history WHERE id = ?", user_id)
        if searchid_row[0]['max_search_id'] is None:
            searchid = 0
        else:
            searchid = searchid_row[0]['max_search_id'] + 1

        if num_results == 0:
            results = db.execute("SELECT * FROM songs ORDER BY ABS(danceability - ?) + ABS(energy - ?) + ABS(speechiness - ?) + ABS(valence - ?) LIMIT 10", danceability, energy, speechiness, valence)

        for i in results:
            db.execute("INSERT INTO history (id, track_id, search_id) VALUES (?, ?, ?)", user_id, i['track_id'], searchid)

        userid = session["user_id"]
        db.execute("UPDATE search SET search = search + 1 WHERE id = ?", userid)

        return render_template("searched.html", results=results, danceability=danceability, energy=energy, speechiness=speechiness, valence=valence)
    else:
        return render_template("apology.html"), 400


@app.route("/history")
@login_required
def history():
    """Show history of song searches"""
    userid = session["user_id"]
    history = db.execute("SELECT DISTINCT h.search_id, s.artists, s.track_name, s.album_name, s.popularity, s.track_genre FROM history h JOIN songs s ON h.track_id = s.track_id WHERE h.id =? ORDER BY h.search_id", userid)

    searches = {}
    for entry in history:
        search_id = entry['search_id']
        if search_id not in searches:
            searches[search_id] = []
        searches[search_id].append(entry)


    return render_template("history.html", searches=searches)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return "Must provide username", 403

        # Ensure password was submitted
        elif not request.form.get("password"):
            return "Must provide password", 403

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["password"], request.form.get("password")
        ):
            return "Invalid username and/or password", 403

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # TODO: Add the user's entry into the database
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if username is None or password is None or username == "" or password == "" or confirmation is None or confirmation == "":
            return render_template("apology.html"), 400
        elif password != confirmation:
            return render_template("apology.html"), 400
        else:
            rows = db.execute("SELECT * FROM users WHERE username = ?", username)
            if len(rows) > 0:
                return render_template("apology.html"), 400
            else:
                password = generate_password_hash(request.form.get("password"))
                db.execute("INSERT INTO users (username,password) VALUES(?,?)", username, password)
                userid = db.execute("SELECT id FROM users WHERE username = ?", username)[0]["id"]
                db.execute("INSERT INTO search (id, luck, find, search) VALUES(?,?,?,?)", userid, 0, 0, 0)
                return redirect("/login"), 200
    else:
        return render_template("register.html")
