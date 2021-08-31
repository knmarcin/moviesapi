# Movies API

API was designed to connect with omdbapi and receive dataset about movie, saving it in inner database.


### Endpoints

* ```GET /movies```
    * Fetching a list with all of the movies already present i application database
    * You can filter by many parameters, and you can use same parameter,
      ex. ```?Director=Jackson&Director=Peter```
    * You can filter by content of JSONField, ex. ```?sort=Year``` ```?sort=imdbVotes``` ```?sort=Release``` etc.
    * Default sorting is by ```-id```
* ```POST /movies``` 
    * ex. ```{"question":"hobbit}```
    * gets data from OMDB API and saves it in inner database, with all the details
    
* ```POST /comments``` 
  * ```{"movie_id: 1, "comment":"example"}``` saves comment in database and it is returned in
  request response.
* ```GET /comments``` Fetches all the comments present in application database


### Tests
Few simple steps has beed created for the app