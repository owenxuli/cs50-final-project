import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
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
    name = db2.execute("SELECT name FROM openings")
    color = db2.execute("SELECT color FROM openings")
    variations = db2.execute("SELECT variations FROM openings")
    return render_template(
        "homepage.html", name=name, color=color, variations=variations
    )


# TO-DO
@app.route("/notation")
@login_required
def notation():
    # this function is defined in helpers.py
    squares = generate_board()
    return render_template("notation.html", squares=squares, board=board)


@app.route("/answer", methods=["GET", "POST"])
@login_required
def answer():
    # this will generate a chess board, where every number represents the number of empty squares
    # and the letters represent the pieces based on standard chess notation
    board_string = "3r3n/1k6/8/B7/4P2Q/8/8/R6K"
    board = chess.Board(board_string)

    # this will generate an svg image of the board that can be displayed on the website
    svg_board = chess.svg.board(board=board, size=800)

    if request.method == "POST":
        # get the answers from the user
        answer1 = request.form.get("answer1")
        answer2 = request.form.get("answer2")
        answer3 = request.form.get("answer3")

        correct_answer1 = "rd8d6"
        correct_answer2 = "Ra1f1"
        correct_answer3 = "Qh4g5"

        # check if the user answered all notations
        if not answer1 or not answer2 or not answer3:
            flash("Please respond all questions.")

        # check if the answers are correct
        if (
            answer1 == correct_answer1
            and answer2 == correct_answer2
            and answer3 == correct_answer3
        ):
            flash("Correct!")
        else:
            flash("Incorrect. Please try again.")

        return render_template("answer.html", svg_board=svg_board)
    else:
        return render_template("answer.html", svg_board=svg_board)


# TO-DO
@app.route("/openings")
@login_required
def openings():
    # we generate a board for the final position of every opening that we describe.
    sd_board = chess.Board("rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR")
    svg_sd_board = chess.svg.board(board=sd_board, size=400)

    rl_board = chess.Board("r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R")
    svg_rl_board = chess.svg.board(board=rl_board, size=400)

    ig_board = chess.Board("r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R")
    svg_ig_board = chess.svg.board(board=ig_board, size=400)

    ck_board = chess.Board("rnbqkbnr/pp1ppppp/2p5/8/4P3/8/PPPP1PPP/RNBQKBNR")
    svg_ck_board = chess.svg.board(board=ck_board, size=400)

    qg_board = chess.Board("rnbqkbnr/ppp1pppp/8/3p4/2PP4/8/PP2PPPP/RNBQKBNR")
    svg_qg_board = chess.svg.board(board=qg_board, size=400)

    return render_template(
        "openings.html",
        sd_board=svg_sd_board,
        rl_board=svg_rl_board,
        ig_board=svg_ig_board,
        ck_board=svg_ck_board,
        qg_board=svg_qg_board,
    )


# TO-DO
@app.route("/rules")
@login_required
def rules():
    # we generate the following boards to show the positions that are described in the rules.html page
    board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
    svg_board = chess.svg.board(board=board, size=400)

    checkmate = chess.Board("4k3/8/8/7r/8/8/5PP1/5RKq")
    svg_checkmate = chess.svg.board(board=checkmate, size=400)

    draws = chess.Board("2k5/8/8/3QB3/8/4K3/8/8")
    svg_draws = chess.svg.board(board=draws, size=400)

    return render_template(
        "rules.html", board=svg_board, checkmate=svg_checkmate, draws=svg_draws
    )


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


@app.route("/simulations")
@login_required
def simulations():
    return render_template("simulations.html")
