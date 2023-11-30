import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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
    """Show portfolio of stocks"""
    # retrieve the stocks and shares purchased by a user from the transactions table
    stocks = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0",
        user_id=session["user_id"],
    )

    # retrieve the cash remaining from the users table
    cash = db.execute(
        "SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"]
    )[0]["cash"]

    total_value = cash
    total = cash

    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["name"] = quote["name"]
        stock["price"] = quote["price"]
        stock["value"] = stock["price"] * stock["total_shares"]
        total_value += stock["value"]

    return render_template(
        "index.html", stocks=stocks, cash=cash, total_value=total_value
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # check if request method is POST
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")

        # check if the user inputted a symbol
        if not symbol:
            return apology("Please provide a symbol")

        # check if the user inputted a valid number of shares
        elif not shares or not shares.isdigit() or int(shares) <= 0:
            return apology(
                "Please provide a valid number of shares",
            )

        # if the inputted symbol and shares are valid, then lookup stock quote
        quote = lookup(symbol)

        # check if the symbol exists
        if quote is None:
            return apology("Symbol not found")

        # if the symbol exists, then calculate the total cost of the number of shares the user wants to buy, and check if the user has enough cash to buy the shares
        price = quote["price"]
        total_cost = int(shares) * price
        user_cash = db.execute(
            "SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"]
        )[0]["cash"]
        if user_cash < total_cost:
            return apology(
                "You do not have enough cash",
            )

        # if the user has enough cash, then update the users table with the remaining cash
        db.execute(
            "UPDATE users SET cash = cash - :cost WHERE id = :user_id",
            cost=total_cost,
            user_id=session["user_id"],
        )

        # to create a new table for the history of transactions for the user, only has to be run once from SQLite3
        # CREATE TABLE transactions (
        #   id INTEGER PRIMARY KEY AUTOINCREMENT,
        #   user_id INTEGER NOT NULL,
        #   symbol TEXT NOT NULL,
        #   shares INTEGER NOT NULL,
        #   price NUMERIC NOT NULL,
        #   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        #   FOREIGN KEY (user_id) REFERENCES users(id)
        # );

        # once the purchase is completed, then update the history of the purchases of the user
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
            user_id=session["user_id"],
            symbol=symbol,
            shares=shares,
            price=price,
        )

        # once bough, redirect to /
        return redirect("/")

    # if the request method is GET, then go to buy.html
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute(
        "SELECT * FROM transactions WHERE user_id = :user_id ORDER BY timestamp DESC",
        user_id=session["user_id"],
    )

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password")

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote:"""
    # check if the request method is POST
    if request.method == "POST":
        # the symbol is going to be the symbol that the user is searching for
        symbol = request.form.get("symbol").upper()

        # lookup the symbol that the user is searching for
        quote = lookup(symbol)

        # if the symbol does not exist, then return error
        if not quote:
            return apology("Invalid symbol")

        # if the symbol does exist, then render quote.html site
        return render_template("quoted.html", quote=quote)

    # if the request method is GET, then render the quote.html site
    else:
        return render_template("quote.html")


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


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # get the stocks of a user
    stocks = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0",
        user_id=session["user_id"],
    )

    # check the request method
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")

        # check if the user selected a symbol before selling
        if not symbol:
            return apology("Please select a symbol")

        # check if the user inputted a valid number of shares
        elif not shares or int(shares) <= 0:
            return apology("Please provide a valid number of shares")

        else:
            shares = int(shares)

        for stock in stocks:
            if stock["total_shares"] < shares:
                return apology("You don't own enough shares")
            else:
                quote = lookup(symbol)
                if quote is None:
                    return apology("Symbol not found")
                price = quote["price"]
                sale = shares * price

                # if the order is valid, then update the users table
                db.execute(
                    "UPDATE users SET cash = cash + :sale WHERE id = :user_id",
                    sale=sale,
                    user_id=session["user_id"],
                )

                # update the history table
                db.execute(
                    "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
                    user_id=session["user_id"],
                    symbol=symbol,
                    shares=-shares,
                    price=price,
                )

                return redirect("/")

    else:
        return render_template("sell.html", stocks=stocks)


# personal touch: add money to account
@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    # check if the request method is post
    if request.method == "POST":
        # set the funds to be added as the number the user inputs
        funds = int(request.form.get("funds"))

        # check what the user has in cash
        user_cash = db.execute(
            "SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"]
        )[0]["cash"]

        # check if the value is valid
        if funds <= 0 or not funds:
            return apology("Please add valid amount of funds")

        # if the funds are valid, then update the users table by adding the user cash and the inserted funds
        else:
            db.execute(
                "UPDATE users SET cash = :user_cash + :funds WHERE id = :user_id",
                user_cash=user_cash,
                funds=funds,
                user_id=session["user_id"],
            )

            # once the funds are added, return to the homepage
            return redirect("/")
    else:
        return render_template("account.html")
