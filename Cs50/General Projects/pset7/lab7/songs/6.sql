--list names of songs which are by post malone
--no assumptions on what his artist ID is (use the other table)
SELECT name FROM songs WHERE artist_id IN( SELECT id FROM artists WHERE name = 'Post Malone');
