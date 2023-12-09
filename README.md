# EnPeassant, by Owen Xu Li and Daniel Zhang

Welcome to our CS50 final project! 

Given that both of us are passionate about chess, we decided to combine our interests in chess and programming to develop an educational website that allows users to learn the rules, the notation, and a selection of common chess openings so that they are up and running to play chess matches with other beginners after visiting the site.

## Getting Started

We used two Python libraries: chess, and chess.svg. So the first step is to import the two libraries by running:
1. python3 -m pip install chess
2. python3 -m pip install chess.svg

We also used Chessboard.js, a free-to-use resource that allows easy implementation of interactive chess boards embedded into websites through JavaScript. In order to download and use Chessboard.js, we went to chessboardjs.com and downloaded the latest version of the code. The folder containing the downloaded files are inside the chessboardjs-1.0.0/ folder, including the license for the usage of the code. To use the Chessboard.js resource, we made copies of the JS, CSS，and image files (in the static/pieces/ folder) in our static/ folder so they are easily accesible. Thus, there is no further need to install any additional resources to run our project, since the files are inside the static/ folder.

To run the program, use "flask run" in the terminal, and enter the server.

Note: to collaborate on the project, we used VS Code and GitHub, so we also had to install some of the libraries pre-installed on the CS50 codespace, such as the cs50 library itself to use the SQL functionality, into our VS Code Desktop version.

Note: we are using Python 3.11.5. At the beginning we were having trouble collaborating since the VS Code of Daniel did not recognize the "flask run" or "pip" commands, but after installing Python 3.11.5 to his computer, all the issues were solved.

After registering a new user and logging in, you can then proceed to use all the subpages freely.

## Understanding

### app.py

From the Finance pset from week 9, we borrowed the login and register functions. We also imported most of the same libraries that the finance pset required, but of course we also imported the chess and chess.svg libraries to generate the chess boards. In app.py, we first configure to use users.db. We used SQL to implement the login and register functions. Notice that the sqlcode.sql file contains the code, that is only needed to be ran once when running sqlite3 in the terminal. The users.db table only contains the id of the user, the username of the user, and the hashed password of the user. In app.py, we also configure to use openings.db, which contains the name, the opening color, and the variations of each of the selected chess openings, which are displayed on the homepage. The code we used to create named table is also inside the sql file.

The chess library generates boards through the chess.Board() function. We specified the location of each of the pieces using the standard chess (UCI) notation described in the notation.html page. In short, the chess.Board() function takes a string as an input; such string must be in the following format: "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", where every letter represents a piece and its color, each number represents the number of spaces before a piece, if any, and every slash represents the beginning of the following row, from the top row down. Afterward, we use the chess.svg library to render the generated boards into svgs and be displayed in our sites. These boards are not interactive, and function more as examples of a certain board position or opening. For practicing, we developed simulations.html, and in app.py, where users can practice the selected openings.

### helpers.py

Aside from the long_required and apology functions, which we borrowed from the finance pset, we also created a function to generate a chess board on standard initial position with the white pieces closest to the user (at the bottom). Notice that we changed the apology image to one of our own selection.

### static/

Inside the static folder, we have our style.css file, which contains all the styling we did to our website so that it looks more appealing. We also have the JavaScript files that some our sites needed for interactive chess boards, buttons, and other functionalities.

### templates/

Inside the templates folder, we have every html file that we created for our project. The most important ones are notation.html, answer.html, openings.html, and simulations.html. In notation.html, you can find a basic tutorial on how standard chess notation is used to describe the movement of a piece from one square to another, and the symbol and names for each piece and each square in the board. This site will then allow you to go to answer.html, which is a basic practice of the chess notation, with 3 forms to be submitted, and each form describing the movement of a specific piece in the board. 