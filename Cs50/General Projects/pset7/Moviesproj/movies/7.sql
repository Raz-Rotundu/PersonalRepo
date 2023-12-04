--list all movies from 2010 in with their ratings in descending order by rating movies with the same rating should be ordered alphabetically
SELECT m.title, r.rating FROM movies AS m
JOIN ratings AS r ON m.id = r.movie_id
WHERE m.year = '2010'
ORDER BY r.rating DESC, m.title;