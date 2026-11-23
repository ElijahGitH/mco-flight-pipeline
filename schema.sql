CREATE TABLE airlines (
    airline_code  VARCHAR(3) PRIMARY KEY,
    airline_name  TEXT
);

CREATE TABLE airports (
    airport_code  CHAR(3) PRIMARY KEY,
    city          TEXT,
    state         CHAR(2)
);

CREATE TABLE flights (
    flight_id           BIGSERIAL PRIMARY KEY,
    flight_date         DATE NOT NULL,
    airline_code        VARCHAR(3) REFERENCES airlines(airline_code),
    flight_number       INT,
    origin              CHAR(3) REFERENCES airports(airport_code),
    dest                CHAR(3) REFERENCES airports(airport_code),
    sched_dep_time      SMALLINT,
    dep_delay_min       NUMERIC,
    arr_delay_min       NUMERIC,
    cancelled           BOOLEAN,
    diverted            BOOLEAN,
    carrier_delay       NUMERIC,
    weather_delay       NUMERIC,
    nas_delay           NUMERIC,
    security_delay      NUMERIC,
    late_aircraft_delay NUMERIC,
    UNIQUE (flight_date, airline_code, flight_number, origin)
);