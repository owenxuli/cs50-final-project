import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import chess
import chess.svg

from helpers import apology, login_required, generate_board

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///users.db")
db2 = SQL("sqlite:///openings.db")

# a global variable for the chess board
board = chess.Board()

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route("/")
@login_required
def homepage():
    name = db2.execute ("SELECT name FROM openings")
    color = db2.execute ("SELECT color FROM openings")
    variations = db2.execute ("SELECT variations FROM openings")
    return render_template("homepage.html", name = name, color = color, variations = variations)


#TO-DO
@app.route("/notation")
@login_required
def notation():
    squares = generate_board()
    
    return render_template('notation.html', squares=squares, board=board)

@app.route("/answer", methods=["GET", "POST"])
@login_required
def answer():
    if request.method == "POST":
        # this function is defined in helpers.py

        answer1 = request.form.get("answer1")
        answer2 = request.form.get("answer2")
        answer3 = request.form.get("answer3")

        correct_answer1 = "rd8f8"
        correct_answer2 = "Ra1a3"
        correct_answer3 = "Qh4e1"
            
        if answer1 == correct_answer1:
            flash("Correct!")
        else:
            flash("Try again!")

        if answer2 == correct_answer2:
            flash("Correct!")
        else:
            flash("Try again!")

        if answer3 == correct_answer3:
            flash("Correct!")
        else:
            flash("Try again!")
        
        return render_template("answer.html")
    else:
        return render_template("answer.html")
        
#TO-DO
@app.route("/openings")
@login_required
def openings():
    return render_template("openings.html")


#TO-DO
@app.route("/rules")
@login_required
def rules():
    return render_template("rules.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

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
    """Register user"""
    # clear the session first
    session.clear()

    # check if the request method is POST
    if request.method == "POST":
        # check if the user provided a username
        if not request.form.get("username"):
            return apology("Please provide a username")

        # check if the user provided a password
        elif not request.form.get("password"):
            return apology("Please provide a password")

        # check if the user provided a confirmation of the password
        elif not request.form.get("confirmation"):
            return apology(
                "Please provide a confirmation for the password",
            )

        # check if the password and confirmation fields have the same input
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology(
                "The passwords do not match",
            )

        # query the database
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # check if the username inputted already exists, since the number of rows with the inputted username should be 0
        if len(user) != 0:
            return apology(
                "Username already exists",
            )

        # if the username does not exist, then insert into users table
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            request.form.get("username"),
            generate_password_hash(request.form.get("password")),
        )

        # query database for newly created user
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # remember the user that is logged in
        session["user_id"] = user[0]["id"]

        # once registered, go back to homepage
        return redirect("/")

    # if the request method is GET, then enter register.html
    else:
        return render_template("register.html")

if __name__ == '__main__':
    app.run(debug=True)