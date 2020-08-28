import string

import sqlite3
import random
from flask import Flask, render_template, request
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

from helper import get_image, get_summary


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

conn = sqlite3.connect(
    'database.db', isolation_level=None, check_same_thread=False)
db = conn.cursor()


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/genre", methods=["GET", "POST"])
def genre():

    if request.method == "POST":

        rating = request.form.get("rating")

        if int(rating) > 10 or int(rating) < 0:
            return render_template("apology.html", msg="Must input valid rating!")

        genre = request.form.get("genre")
        genre = string.capwords(genre)
        genre = genre.replace(" ", "")
        genre = "%"+genre+"%"

        db.execute(
            "SELECT tconst, primaryTitle, startYear, rating FROM movies WHERE genres LIKE ? AND votes > 10000 AND rating > ?", (genre, float(rating),))
        l_genres = db.fetchall()

        if not l_genres:
            return render_template("apology.html", msg="No match found! Check genre/rating!")

        num = random.randint(0, len(l_genres) - 1)

        tconst = l_genres[num][0]
        title = l_genres[num][1]
        year = l_genres[num][2]
        image = get_image(tconst)
        summary = get_summary(tconst)

        return render_template("brewed.html", tconst=tconst, title=title, year=year, image=image, summary=summary)

    else:
        return render_template("genre.html")


@app.route("/brewed2")
def toprated():

    db.execute(
        "SELECT tconst, primaryTitle, startYear FROM movies WHERE votes > 25000 ORDER BY rating DESC LIMIT 250")
    l_genres = db.fetchall()

    num = random.randint(0, len(l_genres) - 1)

    tconst = l_genres[num][0]
    title = l_genres[num][1]
    year = l_genres[num][2]

    image = get_image(tconst)
    summary = get_summary(tconst)

    return render_template("brewed2.html", tconst=tconst, title=title, year=year, image=image, summary=summary)


@app.route("/brewed3")
def mostpopular():

    db.execute(
        "SELECT tconst, primaryTitle, startYear FROM movies ORDER BY votes DESC LIMIT 250")
    l_genres = db.fetchall()

    num = random.randint(0, len(l_genres) - 1)

    tconst = l_genres[num][0]
    title = l_genres[num][1]
    year = l_genres[num][2]

    image = get_image(tconst)
    summary = get_summary(tconst)

    return render_template("brewed3.html", tconst=tconst, title=title, year=year, image=image, summary=summary)


@app.route("/wild")
def wildbrew():

    db.execute(
        "SELECT tconst, primaryTitle, startYear FROM movies WHERE votes > 50000 ORDER BY rating DESC, startYear DESC LIMIT 500")
    l_genres = db.fetchall()

    num = random.randint(0, len(l_genres) - 1)

    tconst = l_genres[num][0]
    title = l_genres[num][1]
    year = l_genres[num][2]

    image = get_image(tconst)
    summary = get_summary(tconst)

    return render_template("wild.html", tconst=tconst, title=title, year=year, image=image, summary=summary)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template("apology.html", msg="Internal Server Error")


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
