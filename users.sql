/* only needs to be ran once to create the database to store the users */

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
    username TEXT NOT NULL, 
    hash TEXT NOT NULL);

CREATE UNIQUE INDEX username ON users (username);