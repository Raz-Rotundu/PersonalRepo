-- Keep a log of any SQL queries you execute as you solve the mystery.

--.schema checking what data we have
.schema

--find the c.s report for stolen duck
SELECT * FROM crime_scene_reports AS csr
WHERE csr.description LIKE '%CS50%';
    --Happened at 2021.07.28 at 10:15am
    --Humphrey st. bakery
    --3 interviews which mention the Humphrey Street bakery

--find the 3 interviews
SELECT i.month, i. day, i.name, i.transcript FROM interviews AS i
WHERE i.transcript LIKE '%bakery%';
    --Ruth: thief got away in a car within 10 mins of theft, check security footage
    --Eugene: thief is someone he recognized, was withdrawing money at Leggett st. ATM prior to interview this morning(when?)
    --Raymond: Thief called someone for < 1 min. Accomplice is buying a flight ticket for earliest flight out tomorrow, thief will be on it

--check the security footage, filter by date and minute
SELECT * FROM bakery_security_logs AS bsl
WHERE bsl.year = 2021 AND bsl.month = 07 AND bsl.day = 28 AND bsl.hour = 10 AND bsl.minute < 25 AND bsl.minute >15;
    --we now have a list of suspect license plates

--Find all people who are associated with the plates, and who withdrew money from the Leggett st. ATM
SELECT DISTINCT p.name FROM people AS p
JOIN bank_accounts  AS ba ON p.id = ba.person_id
JOIN atm_transactions AS a ON ba.account_number = a.account_number
JOIN bakery_security_logs AS bsl ON p.license_plate = bsl.license_plate
WHERE bsl.year = 2021 AND bsl.month = 07 AND bsl.day = 28 AND bsl.hour = 10 AND bsl.minute < 25 AND bsl.minute >15
AND a.atm_location LIKE '%Leggett%' AND a.transaction_type = 'withdraw';
    --Suspects: Bruce, Luca, Iman, Diana

--Of these 4, who made a call <1 Duration in length?
SELECT p.name FROM people AS p
INNER JOIN phone_calls AS pc ON p.phone_number = pc.caller
WHERE pc.duration < '60';

--Find all people who are associated with the plates, and who withdrew money from the Leggett st. ATM, and who made a call <60 seconds in duration
SELECT DISTINCT p.name FROM people AS p
JOIN bank_accounts  AS ba ON p.id = ba.person_id
JOIN atm_transactions AS a ON ba.account_number = a.account_number
JOIN bakery_security_logs AS bsl ON p.license_plate = bsl.license_plate
JOIN phone_calls AS pc ON p.phone_number = pc.caller
WHERE bsl.year = 2021 AND bsl.month = 07 AND bsl.day = 28 AND bsl.hour = 10 AND bsl.minute < 25 AND bsl.minute >15
AND a.atm_location LIKE '%Leggett%' AND a.transaction_type = 'withdraw'
AND pc.duration <= '60';
    --Suspects: Bruce, Diana

--Of the suspects, find the one who took a flight out of fiftyville and give destination, pick the earliest one if multiple
SELECT DISTINCT p.name FROM people AS p
JOIN bank_accounts  AS ba ON p.id = ba.person_id
JOIN atm_transactions AS a ON ba.account_number = a.account_number
JOIN bakery_security_logs AS bsl ON p.license_plate = bsl.license_plate
JOIN phone_calls AS pc ON p.phone_number = pc.caller
JOIN passengers AS pass ON p.passport_number = pass.passport_number
JOIN flights AS f ON pass.flight_id = f.id
JOIN airports AS ap ON f.origin_airport_id = ap.id --we want to find who left fiftyville
WHERE bsl.year = 2021 AND bsl.month = 07 AND bsl.day = 28 AND bsl.hour = 10 AND bsl.minute < 25 AND bsl.minute >15 --people in suspicious time
AND a.atm_location LIKE '%Leggett%' AND a.transaction_type = 'withdraw' -- Intersect people who withdrew from legget
AND pc.duration <= '60' --Intersect people who made a short call
AND ap.city LIKE '%Fiftyville%'; --Intersect people on a flight out of fiftyville
    --Still Bruce and Diana!

--Find out the time of the flight out
SELECT DISTINCT p.name, f.year, f.month, f.day, f.hour FROM people AS p
JOIN bank_accounts  AS ba ON p.id = ba.person_id
JOIN atm_transactions AS a ON ba.account_number = a.account_number
JOIN bakery_security_logs AS bsl ON p.license_plate = bsl.license_plate
JOIN phone_calls AS pc ON p.phone_number = pc.caller
JOIN passengers AS pass ON p.passport_number = pass.passport_number
JOIN flights AS f ON pass.flight_id = f.id
JOIN airports AS ap ON f.origin_airport_id = ap.id --we want to find who left fiftyville
WHERE bsl.year = 2021 AND bsl.month = 07 AND bsl.day = 28 AND bsl.hour = 10 AND bsl.minute < 25 AND bsl.minute >15 --people in suspicious time
AND a.atm_location LIKE '%Leggett%' AND a.transaction_type = 'withdraw' -- Intersect people who withdrew from legget
AND pc.duration <= '60' --Intersect people who made a short call
AND ap.city LIKE '%Fiftyville%'; --Intersect people on a flight out of fiftyville
    --Bruce took the earliest flight on the 29th it must be him

--Find out Bruce's destination
SELECT DISTINCT p.name, ap.full_name FROM people AS p
JOIN bank_accounts  AS ba ON p.id = ba.person_id
JOIN atm_transactions AS a ON ba.account_number = a.account_number
JOIN bakery_security_logs AS bsl ON p.license_plate = bsl.license_plate
JOIN phone_calls AS pc ON p.phone_number = pc.caller
JOIN passengers AS pass ON p.passport_number = pass.passport_number
JOIN flights AS f ON pass.flight_id = f.id
JOIN airports AS ap ON f.destination_airport_id = ap.id --we want to find who left fiftyville
WHERE bsl.year = 2021 AND bsl.month = 07 AND bsl.day = 28 AND bsl.hour = 10 AND bsl.minute < 25 AND bsl.minute >15 --people in suspicious time
AND a.atm_location LIKE '%Leggett%' AND a.transaction_type = 'withdraw' -- Intersect people who withdrew from legget
AND pc.duration <= '60' --Intersect people who made a short call
AND p.name = 'Bruce';
    --Bruce is on his way to LaGuardia Airport(New York)

--Find out what Bruce's number is
SELECT p.name, p.phone_number FROM people AS p
WHERE p.name = 'Bruce';
    --(367) 555-5533

--Find out who he called on the day of the crime
SELECT p.name FROM people AS p
JOIN phone_calls AS pc ON p.phone_number = pc.receiver
WHERE pc.caller = '(367) 555-5533'
AND  pc.year = 2021 AND pc.month = 07 AND pc.day = 28
AND pc.duration < '60';
    --Accomplice is Robin