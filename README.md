# 🚀 Real-Time Crypto ETL Pipeline

An automated ETL (Extract, Transform, Load) pipeline that collects live cryptocurrency prices every minute, transforms the data, and loads it into a PostgreSQL data warehouse using a star schema design — fully orchestrated with Apache Airflow and containerized with Docker.

---

## 📌 Project Overview

This pipeline tracks real-time prices for **8 cryptocurrencies** (Bitcoin, Ethereum, Solana, BNB, XRP, Tether, USDC, TRON) from the CoinGecko API, stores them in a structured PostgreSQL database, and enables historical price analytics.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core pipeline logic |
| Pandas | Data transformation |
| SQLAlchemy | Database connection & ORM |
| PostgreSQL | Data warehouse |
| Apache Airflow | Pipeline orchestration & scheduling |
| Docker | Containerization |
| CoinGecko API | Live cryptocurrency price data |

---

## ⚙️ Pipeline Architecture

```
CoinGecko API
     ↓
 run_extract         → Fetches live prices for 8 coins
     ↓
 run_transform       → Structures data into a DataFrame with timestamps
     ↓
 run_load            → Loads into PostgreSQL star schema
     ↓
 PostgreSQL DWH      → fact_crypto_prices + coin_dim + date_dim
```

Runs every minute via Airflow's `DeltaDataIntervalTimetable`.

---

## 📊 Data Model (Star Schema)

```
        coin_dim
        --------
        coin_id (PK)
        coin_name
             |
             |
fact_crypto_prices -------- date_dim
------------------          --------
id (PK)                     date_id (PK)
coin_id (FK)                full_date
date_id (FK)                day
price                       month
last_updated                year
```

### Tables

**`coin_dim`** — Coin reference data
- `coin_id` — primary key
- `coin_name` — name of the cryptocurrency

**`date_dim`** — Date hierarchy
- `date_id` — primary key
- `full_date` — full date
- `day`, `month`, `year` — date components

**`fact_crypto_prices`** — Price facts (grows every minute)
- `coin_id` — foreign key to `coin_dim`
- `date_id` — foreign key to `date_dim`
- `price` — USD price at time of capture
- `last_updated` — exact timestamp of the record

---

## 📁 Project Structure

```
crypto_pipeline_project/
├── dags/
│   └── crypto_pipeline.py   # Airflow DAG definition
├── extract.py               # Fetches data from CoinGecko API
├── transform.py             # Transforms raw JSON into DataFrame
├── load.py                  # Loads data into PostgreSQL
├── main.py                  # Local run entry point
├── schema.sql               # Database schema
├── docker-compose.yml       # Docker setup
└── README.md
```

---

## 🔄 ETL Steps

### Extract (`extract.py`)
- Hits CoinGecko's `/simple/price` endpoint
- Fetches prices for all 8 coins in one request
- Retries up to 3 times for any missing coins with a 2-second delay between retries

### Transform (`transform.py`)
- Converts raw JSON response into a structured pandas DataFrame
- Adds a `time_stamp` column with the current datetime
- Maps API coin IDs to display names (e.g. `binancecoin` → `bnb`)

### Load (`load.py`)
- Auto-inserts new coins into `coin_dim` if not already present
- Auto-inserts new dates into `date_dim` if not already present
- Merges `coin_id` and `date_id` into the DataFrame
- Appends records to `fact_crypto_prices` every minute

---

## 📈 Sample SQL Queries

**Latest price for each coin:**
```sql
SELECT DISTINCT ON (coin_id)
    c.coin_name,
    f.price,
    f.last_updated
FROM fact_crypto_prices f
JOIN coin_dim c ON f.coin_id = c.coin_id
ORDER BY coin_id, last_updated DESC;
```

**High / Low / Average per coin today:**
```sql
SELECT
    c.coin_name,
    MAX(f.price) AS high,
    MIN(f.price) AS low,
    ROUND(AVG(f.price)::numeric, 2) AS average
FROM fact_crypto_prices f
JOIN coin_dim c ON f.coin_id = c.coin_id
JOIN date_dim d ON f.date_id = d.date_id
WHERE d.full_date = CURRENT_DATE
GROUP BY c.coin_name
ORDER BY high DESC;
```
---

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.12+

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/crypto-etl-pipeline.git
cd crypto-etl-pipeline
```

### 2. Start Docker containers
```bash
docker-compose up airflow-init   # first time only
docker-compose up
```

### 3. Access Airflow UI
Open `http://localhost:8080` and log in with:
- Username: `admin`
- Password: `admin`

### 4. Enable the DAG
Find `crypto_pipeline` in the DAG list and toggle it on — it will start running every minute automatically.

### 5. Access the database
```bash
docker exec -it <postgres_container> psql -U airflow -d rtcpp
```

---

## ⚠️ Known Limitations

- CoinGecko free API updates prices every **60 seconds** — running more frequently won't yield new data
- Free API occasionally rate-limits requests — pipeline retries automatically handle this
- If Docker stops, pipeline stops and data will have a gap for that period (`catchup=False`)
- Free API does not provide historical data — gaps cannot be backfilled with accurate prices

---

## 🔮 Future Improvements

- [ ] Add Grafana or Power BI dashboard for visualization
- [ ] Migrate to CoinGecko paid API for faster updates
- [ ] Add data quality checks with Great Expectations
- [ ] Deploy on AWS/GCP for 24/7 uptime
- [ ] Add email/Slack alerts on pipeline failure
- [ ] Implement WebSocket streaming for millisecond-level data

---

## 👤 Author

**Ram** — Data Engineering Enthusiast

[Linkedin](https://www.linkedin.com/in/ram-prasad-b48329292/)

---

## 📄 License

MIT License — feel free to use and build on this project.
```
