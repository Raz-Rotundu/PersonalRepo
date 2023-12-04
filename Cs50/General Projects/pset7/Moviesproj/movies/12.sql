--list titles of all movies in which Johnny Depp and Helena Bonham Carter starred

--1. List all movies in which Johnny Depp Starred
/*SELECT title FROM movies AS m
JOIN stars AS s ON m.id = s.movie_id
JOIN people AS p ON s.person_id = p.id
WHERE p.name = 'Johnny Depp';

--2. List all movies in which Helena Bonham Carter Starred
SELECT title FROM movies AS m
JOIN stars AS s ON m.id = s.movie_id
JOIN people AS p ON s.person_id = p.id
WHERE p.name = 'Helena Bonham Carter';*/

--Now Just inner Join the two results to get overlap(how?)
SELECT title FROM movies AS m
JOIN stars AS s ON m.id = s.movie_id
JOIN people AS p ON s.person_id = p.id
WHERE p.name = 'Johnny Depp' AND m.title IN(
    SELECT title FROM movies AS m
    JOIN stars AS s ON m.id = s.movie_id
    JOIN people AS p ON s.person_id = p.id
    WHERE p.name = 'Helena Bonham Carter'
);
