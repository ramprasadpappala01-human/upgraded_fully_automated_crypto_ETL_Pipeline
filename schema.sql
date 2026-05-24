--create coin dimension table
CREATE TABLE coin_dim(
    coin_id SERIAL PRIMARY KEY,
    coin_name VARCHAR(50) UNIQUE NOT NULL
);
--create date dimension table
CREATE TABLE date_dim(
    date_id SERIAL PRIMARY KEY,
    full_date DATE NOT NULL,
    day INT,
    month INT,
    year INT
);

--create fact table
CREATE TABLE fact_crypto_prices(
    id SERIAL PRIMARY KEY,
    coin_id INT REFERENCES coin_dim(coin_id),
    date_id INT REFERENCES date_dim(date_id),
    price numeric,
    last_updated TIMESTAMP
);
