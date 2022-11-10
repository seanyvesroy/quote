-- $ sqlite3 ./var/quotes.db < ./share/quotes.sql

PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS quotes;
CREATE TABLE quotes (
    id INTEGER primary key,
    genre VARCHAR,
    author VARCHAR,
    title VARCHAR,       
    text VARCHAR,
    UNIQUE(text)
);
INSERT INTO quotes(genre, author, title, text) VALUES('Fantasy','Brandon Sanderson','Oathbringer','Sometimes a hypocrite is nothing more than a man in the process of changing.');

COMMIT;