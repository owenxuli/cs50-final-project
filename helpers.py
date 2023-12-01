import csv
import datetime
import pytz
import requests
import subprocess
import urllib
import uuid

from flask import redirect, render_template, session
from functools import wraps

# this function will generate a chess board
def generate_board():
    board = chess.Board()
    squares = []

    for row in range(7, -1, -1):
        for col in range(8):
            square_name = chess.square_name(chess.square(col, row))
            piece = board.piece_at(chess.square(col, row))
            piece_symbol = piece.symbol() if piece else ""
            color = "white" if (row + col) % 2 == 0 else "black"
            squares.append({"name": square_name, "piece": piece_symbol, "color": color})

    return squares

def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function
