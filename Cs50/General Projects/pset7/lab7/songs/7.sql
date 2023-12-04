--return average energy of Drake's songs don't directly reference artist_id
SELECT AVG(energy) FROM songs WHERE artist_id IN( SELECT id FROM artists WHERE name = 'Post Malone')