# Queries File for SQL queries to be used by main and functions files

"""
SQL queries written as python strings.
Uses python string formatting % for dynamic values.
"""

viewFilm = """
SELECT f.FilmName, a.ActorName
FROM film as f
INNER JOIN filmcast as fc
ON f.FilmID = fc.CastFilmID
INNER JOIN actor as a
ON a.ActorID = fc.CastActorID
ORDER BY f.FilmName ASC, a.ActorName ASC;
"""

actorByYear = """
SELECT ActorName, MONTHNAME(ActorDOB) as Month, ActorGender
FROM actor
WHERE YEAR(ActorDOB) = '%s'
ORDER BY ActorName;
"""

actorByYearWithGender = """
SELECT ActorName, MONTHNAME(ActorDOB) as Month, ActorGender
FROM actor
WHERE YEAR(ActorDOB) = '%s' AND
ActorGender = '%s'
ORDER BY ActorName;
"""

viewStudios = """
SELECT *
FROM studio
ORDER BY StudioID asc;
"""

addNewCountry = """
INSERT INTO Country
VALUES (%s, '%s');
"""

moviesWithSubtitles = """
SELECT FilmName as Name, SUBSTRING(FilmSynopsis,1,30) as Synopsis
from film
where FilmID IN (%s);
"""

movieExists = """
SELECT FilmID
FROM film
WHERE FilmID = %s;"""