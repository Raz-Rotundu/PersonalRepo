--list titles and release years of harry potter movies in chronological order
--SELECT title, year FROM movies WHERE title LIKE 'Harry Potter%' ORDER BY title;

--try two
SELECT m.title, m.year
FROM movies AS m
WHERE m.title LIKE 'Harry Potter%' ORDER BY m.year;