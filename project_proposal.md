## Capstone 1 
### Project Proposal for “TV-series club” 
The goal is to build a database-driven website from an external API. This small application is planned to be like a notebook for TV-Series fans to keep track of watched series and plan the next TV-series to watch.  

This application will allow TV-series (TV-shows) lovers:

    - get information about shows (where to watch, year of release, average rating, etc);

    - create and manage own comments to shows;

    - create and manage personal collections  (for example, "best mini tv-shows", “want to watch”, “favorites”); 

    - have access to all tv-club collections and comments.

To realise these functionality the database for this application will contain tables: 
    - users
    - shows
    - collections
    - comments

    (See the dataschema in tvclub_diagram.png file) 

The application will not be collecting any sensitive information.  But before getting access to the application any user should create an account and login. Authorization/authentication will allow the application to keep track of the given user collections and comments. 

The application will allow logged-in users:

    - search TV-shows by name;

    - open pages with detailed information about the show;

    - contains links to the official websites of tv-shows, that allows user go and watch a show or get more information about the show;

    - create and manage personal collections (they will be shared with other users, but only the author of a collection could be able to delete or edit this collection);

    - create and manage comments to shows (they will be shared with other users, but only the author of a comment could be able to delete or edit this comment);

    - read all comments for a chosen show;

    - familiarize with all collections and comments from any application user.
  
    
For this application I will plan to use a free API. I realize  that the reliability of a free API could be questionable (waiting time, information completeness), so in the application I will try manage user's expectations.


To this application could be also added:
    - likes to somebodies comments or collections (it will allow to display the most popular collections first);
    - genres tags to the collections;
    - in user’s profile could be added preferred genres, and the app could open collections in order that satisfies user’s preferences;
    - add a personal rate to a show (within a comment).


 

