# Movies API

API was designed to connect with omdbapi and receive dataset about movie, saving it in inner database.


### Endpoints

* ```GET /movies```
    * Fetching a list with all of the movies already present i application database
    * You can filter by many parameters, and you can use same parameter,
      ex. ```?Director=Jackson&Director=Peter```
* ```POST /movies``` 
    * ex. ```{"question":"hobbit}```
    * gets data from OMDB API and saves it in inner database, with all the details
    
* ```POST /comments``` yet not implemented
* ```GET /comments``` yet not implemented


### Tests
Few simple steps has beed created for the app