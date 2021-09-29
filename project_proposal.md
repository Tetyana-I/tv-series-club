## Capstone 1 
### Project Proposal for “TV-series club” 
The goal is to build a database-driven website from an external API. This small application is planned to be like a notebook for TV-Series fans to keep track of watched series and plan the next TV-series to watch.  

This application will allow TV-series (TV-shows) lovers:


- get information about shows (where to watch, year of release, number of seasons, average rating, etc)
- rate and review shows
- add to “want to watch” and  “favorites”  lists
- create personal collections  (for example, "best mini tv-series") 

To realise these functionality the database for this application will contain tables: 
- users
- shows
- reviews
- collections
- notes
- favorites
- want_to_see
(see the dataschema in database file) 

The application will not be collecting any sensitive information.  But before getting access to the application any user should create an account and login. Authorization/authentication will allow the application to keep track of the given user preferences and activities. 

The application will allow logged-in users:
- search TV-shows by name
- open pages with detailed information about the show
- add a show to / delete a show from  "Favorites" and "Want-To-See" collections
- create and manage personal collections (they will be shared with other users, but only the author of a collection could be able to delete or edit this collection)
- rate the show and add a review
- read all reviews for the show from any user
- to read all reviews for all shows, created by other application users

For this application I will plan to use a free API. I realize  that the reliability of a free API could be questionable (waiting time, information completeness), so in my application I will try to minimize the number of requests to the external API and manage user's expectations.


To this application could be also added:
- likes to somebodies reviews or collections
- search by different parameters (for example, by genre)
- in user’s profile could be added preferred genres, and the app could open homepage with the recently added tv-shows that satisfies user’s preferences


 

