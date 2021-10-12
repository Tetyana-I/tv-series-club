# TV-Series Club
TV-Series Club project was developed as a part of the Springboard Software Engineering curriculum. The project was designed as a database-driven website from an external API. This project was completed in approximately 35 hours. 

This small application could be used by TV-Series fans as a place to keep track of their favorite TV-series, plan the next TV-series to watch, share their opinion and look for recommendations. 

## Technologies Used

**Front End:** Bootstrap

**Back End:** Python, Flask, SQLAlchemy, WTForms

**Database:** PostgreSQL

**API reference:** TV-Maze (https://www.tvmaze.com/api)

## Deployment
https://tv-series-club.herokuapp.com

## Local Deployment
**Requirements:** Python-3.8.10, Pip, PostgreSQL

1) Initialize PostgreSQL. Create a database named tvclub_db:

    `createdb tvclub_db`

2) Clone Repository

   `git clone https://github.com/Tetyana-I/tv-series-club`

3) Switch to application directory

   `cd tv-series-club`

4) Create and activate virtual environment

    `python3 -m venv venv`

    `source venv/bin/activate`

5) Install dependencies

    `pip install -r requirements.txt`

6) Run application with Flask

    `flask run`

7) Open the application in your browser at

    `https://localhost:<num_of_port>/`



## Features

The TV-series club application allows logged-in users:

- search TV-shows by name;
- open pages with detailed information about the shows that contains links to the official websites of tv-shows;

    ![show details](/static/images/show.png)

- create and manage own comments to shows; they will be shared with other users, but only the author of a comment could be able to delete or edit this comment);
- create and manage personal collections  (for example, "best mini tv-shows", “want to watch”, “favorites”); they will be shared with other users, but only the author of a collection could be able to delete or edit this collection);
- have access to all tv-club collections and comments.

## Tests

Tests were implemented with Unittest Framework. 

    `python -m unittest tests/<name_of_testfile>`


