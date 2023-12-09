/* only needs to be ran once to create the database to store the users */

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
    username TEXT NOT NULL, 
    hash TEXT NOT NULL);

CREATE UNIQUE INDEX username ON users (username);


/* the following code was used to create the table about the chess openings displayed on the homepage */

CREATE TABLE openings (
    name TEXT NOT NULL, 
    color TEXT NOT NULL, 
    variations INTEGER NOT NULL);