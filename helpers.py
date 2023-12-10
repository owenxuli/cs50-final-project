import chess
import chess.svg

from flask import redirect, render_template, session
from functools import wraps

# this function will generate a chess board
def generate_board():
    board = chess.Board()
    squares = []

    for row in range(7, -1, -1):
        for col in range(8):
            # this variable will contain the name for each square, by combining the column and the row to which the square belongs to
            square_name = chess.square_name(chess.square(col, row))

            # this variable contains information about which piece is in each square ath the starting position
            piece = board.piece_at(chess.square(col, row))

            # this variable is the symbol of each piece
            piece_symbol = piece.symbol() if piece else ""

            # this variable is the color of each square
            color = "white" if (row + col) % 2 == 0 else "black"

            # this will combine the information of the square name, the piece symbol, and the square color so that it can be displayed on the board
            squares.append({"name": square_name, "piece": piece_symbol, "color": color})

    return squares

def apology(message, code=400):
    """Render message as an apology to user."""
    return render_template("apology.html", code=code, message=message)


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
