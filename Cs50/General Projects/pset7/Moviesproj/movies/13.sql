--list the names of all people which starred in a movie in which Kevin Bacon Also Starred. Specify his birthdate as 1958

--1.select all movies in which K.B(1958) starred
/*SELECT title FROM movies AS m
JOIN stars AS s ON m.id = s.movie_id
JOIN people AS p ON s.person_id = p.id
WHERE p.name = 'Kevin Bacon' AND p.birth = '1958';

--2.select all names which participated in a named movie ("The Godfather)
SELECT p.name FROM people AS p
JOIN stars AS s ON p.id = s.person_id
JOIN movies AS m ON s.movie_id = m.id
WHERE m.title = 'The Godfather';*/

--run 2. with 1. nested inside
SELECT p.name FROM people AS p
JOIN stars AS s ON p.id = s.person_id
JOIN movies AS m ON s.movie_id = m.id
WHERE NOT p.name = 'Kevin Bacon'
AND m.title IN(
    SELECT title FROM movies AS m
    JOIN stars AS s ON m.id = s.movie_id
    JOIN people AS p ON s.person_id = p.id
    WHERE p.name = 'Kevin Bacon' AND p.birth = '1958'
);