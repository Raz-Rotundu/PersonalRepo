--Average rating of all movies from 2012
SELECT AVG(rating) FROM ratings WHERE movie_id IN(
    SELECT id FROM movies WHERE year = '2012'
);