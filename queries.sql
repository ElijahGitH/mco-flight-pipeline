-- 1. Which airlines are most delayed arriving/departing MCO?
SELECT a.airline_name,
       COUNT(*) AS flights,
       ROUND(AVG(f.arr_delay_min), 1) AS avg_arrival_delay
FROM flights f
JOIN airlines a ON a.airline_code = f.airline_code
WHERE NOT f.cancelled
GROUP BY a.airline_name
ORDER BY avg_arrival_delay DESC;

-- 2. What hour of the day is worst to fly out of MCO?
SELECT f.sched_dep_time / 100 AS departure_hour,
       COUNT(*) AS flights,
       ROUND(AVG(f.dep_delay_min), 1) AS avg_departure_delay
FROM flights f
WHERE f.origin = 'MCO' AND NOT f.cancelled
GROUP BY departure_hour
ORDER BY departure_hour;

-- 3. Cancellation rate by airline
SELECT a.airline_name,
       COUNT(*) AS flights,
       ROUND(100.0 * SUM(CASE WHEN f.cancelled THEN 1 ELSE 0 END) / COUNT(*), 2) AS pct_cancelled
FROM flights f
JOIN airlines a ON a.airline_code = f.airline_code
GROUP BY a.airline_name
ORDER BY pct_cancelled DESC;

-- 4. Top 10 destinations from MCO
SELECT ap.city, ap.state,
       COUNT(*) AS flights,
       ROUND(AVG(f.arr_delay_min), 1) AS avg_arrival_delay
FROM flights f
JOIN airports ap ON ap.airport_code = f.dest
WHERE f.origin = 'MCO'
GROUP BY ap.city, ap.state
ORDER BY flights DESC
LIMIT 10;

-- 5. What causes the delays? (total minutes by cause)
SELECT SUM(carrier_delay)       AS airline_caused,
       SUM(weather_delay)       AS weather,
       SUM(nas_delay)           AS air_traffic_system,
       SUM(security_delay)      AS security,
       SUM(late_aircraft_delay) AS late_incoming_plane
FROM flights;