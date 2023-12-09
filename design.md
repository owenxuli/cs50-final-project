# Project Design

## homepage.html

This site contains a table listing some of our own favorite chess openings. If you click on each of the openings, you will be redirected to a website (wikipedia) where you can find more information about the history and general information on the opening. This page also contains information about which color chooses to initiate the opening, and how many main variations of the opening exist. Under this table, there is a seemingly normal chessboard, however, we have eliminated all the legal functions that is chess rules, so you can try to drag pieces around in anyway you want! Once, you are satisfied with your position, you can click the restart button underneath which will revert the board back to its original position. 

## notation.html 

The purpose of this project was to design a website to help beginner chess enthusiasts, like us, learn to navigate the game of chess. This page introduces the written notation that chess players use to describe motion on a chessboard. We provide a chessboard that indicates what each square on the board is called, as well as how each piece is differentiated between the two colors. As learners, nobody is expected to understand everything just by reading, so we provided a link to answer.html which will be explained in the section below. 

## answer.html

This site is a follow-up of notation.html. We delivered a board with a set position, the aim of the user is to follow the instructions given in each textbox indicating a move by a specific piece. The user can test their knowledge by attempting to fill in the correct responses for each corresponding textbox with the notation they learned in notation.html. We decided to implement this with a form, so that users can type the answer instead of dragging to the target square, since we believe it is better practice to write the notation than to see it.

## openings.html

Given the openings in homepage.html, we want to see what the position looks like on a chessboard. This page offers an image of each opening and their basic informations which include: move order, pros vs cons, and chess masters who play this opening. We implemented a vertical menu bar that enables users to click on the opening of their choice and learn about them. To aid the understanding of our users further, we intentionally inputted the letters and numbers associated with the chessboard within the board frame. This additional feature makes visualizing the move order an easier process. 

## rules.html

In this site, we give an overview of the chess rules. Through the use of boards in various situations, we were able to provide what a checkmate or draw looks like. There contains no interactive features on this page, as its purpose is solely to provide information to those who are not familiar with the rules already, or to answer any skepticism the user had. 

## simulations.html

The simulations page borrows the sidebar menu implemented in the openings page, but this time we wanted to let the user experience how the opening evolves, and when either Black or White can choose to accept or reject the opening. We decided to implement this with buttons so that users spend less time thinking about the notation and manually moving the pieces to their target squares, and just practice the opening. Notice that the buttons don't need to be clicked in order, but that in order to reach the full position, every button has to be clicked; we did this purposefully since we believe it lets users experiment with the pieces and visualize the impact of each piece on the board without interference from the other pieces. Of course, the original purpose is to click the buttons from left to right in order, and once done, click the Start Postition to start over and keep experimenting or practicing the opening.

## layout.html 

The layout page provides the format used by all of our html pages. This mainly concerns the top tabs on each page that can take the user to their corresponding page upon being clicked. The other functions inlcude making the page compatible with mobile devices, utilizing boostrap to format the tables such as the one in homepage.html to look clean, and format the title with body sections. We also used bootstrap in our project, and we included two css files: one for the general design of teh website in the style.css file, and one from the chessboard.js resource to decorate the chess boards.

## apology.html

Similar to the apology.html we utilized in the finance pset. We changed the picture from the cat to a picture of the previous World Champion, Magnus Carlsen. 