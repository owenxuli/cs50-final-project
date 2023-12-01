import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import chess

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///users.db")


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
    return render_template("homepage.html")


#TO-DO
@app.route("/notation")
@login_required
def notation():
    return render_template("notation.html")


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

    # Get the inputs from the register page

    username = request.form.get("username")

    password = request.form.get("password")
    
    confirmation = request.form.get("confirmation")
    
    if request.method == "GET":
        return render_template("register.html")
    
    elif not username:
        # When there is no inputted username
        return apology("No Input Username")
    
    elif not password or not confirmation:
        # When there is no inputted password or confirmation
        return apology("Password or Confirmation Left Blank")
    
    elif password != confirmation:
        # When the inputted password doesn't match the confirmation password
        return apology("Passwords Didn't Match")
    
    # Using the generate_password_hash to encrypt the password into something harder to hack
    npassword = generate_password_hash(password)
    try:
        # Inserting the username and the encrypted password into the users table
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)", username, npassword
        )
    
    except:
        # Unless the username already exists
        return apology("Username Already Exists")

    # Redirect to the homepage when finished
    return redirect("/")
