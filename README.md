# EnPeassant, by Owen Xu Li and Daniel Zhang

Welcome to our CS50 final project! 

Given that both of us are passionate about chess, we decided to combine our interests in chess and programming to develop an educational website that allows users to learn the rules, the notation, and a selection of common chess openings so that they are up and running to play chess matches with other beginners after visiting the site.

## Getting Started

We used two Python libraries: chess, and chess.svg. So the first step is to import the two libraries by running:
1. python3 -m pip install chess
2. python3 -m pip install chess.svg

To run the program, use "flask run" in the terminal, and enter the server.

Note: to collaborate on the project, we used VS Code and GitHub, so we also had to install some of the libraries pre-installed on the CS50 codespace, such as the cs50 library itself to use the SQL functionality.

After registering a new user, you can then proceed to use all the subpages freely.

## Understanding

### app.py

From the Finance pset from week 9, we borrowed the login and register functions. We also imported most of the same libraries that the finance pset required, but of course we also imported the chess and chess.svg libraries to generate the chess boards. In app.py, we first configure to use users.db. We used SQL to implement the login and register functions. Notice that the users.sql file contains the code, that is only needed to be ran once when running sqlite3 in the terminal. The users.db table only contains the id of the user, the username of the user, and the hashed password of the user. In app.py, we also configure to use openings.db, which contains the name, the opening color, and the variations of each of the selected chess openings, which are displayed on the homepage. The code we used to create named table is also inside the sql file.

### helpers.py

Aside from the long_required and apology functions, which we borrowed from the finance pset, we also created a function to generate a chess board on standard initial position with the white pieces closest to the user (at the bottom). Notice that we changed the apology image to one of our own selection.

### static/

Inside the static folder, we have our style.css file, which contains all the styling we did to our website so that it looks more appealing.