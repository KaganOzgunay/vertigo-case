# Vertigo Games - Case Study

This repository contains solutions for both parts of the Vertigo Games case study.

---

## Part 1: Clans Management API

A REST API for managing game clans, built with FastAPI and MySQL.

## Technology Stack

- **Framework**: Python 3.11 + FastAPI
- **Database**: MySQL 8.0
- **ORM**: SQLAlchemy 2.0
- **Containerization**: Docker
- **Cloud Deployment**: Google Cloud Run + Cloud SQL (optional)

## Project Structure

```
vertigo-case/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Environment configuration
│   ├── database.py          # SQLAlchemy setup
│   ├── models/
│   │   └── clan.py          # Clan ORM model
│   ├── schemas/
│   │   └── clan.py          # Pydantic request/response schemas
│   ├── routers/
│   │   └── clans.py         # API endpoints
│   └── services/
│       └── clan_service.py  # Business logic layer
├── scripts/
│   └── import_data.py       # CSV data import script
├── data/
│   └── clan_sample_data.csv # Sample data (50 records)
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Quick Start (Local with Docker)

The easiest way to run this project locally is with Docker Compose. No cloud account required.

### Prerequisites

- Docker and Docker Compose installed

### Step 1: Start the Services

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/vertigo-case.git
cd vertigo-case

# Start API and MySQL database
docker-compose up -d

# Check logs
docker-compose logs -f api
```

### Step 2: Import Sample Data

```bash
docker-compose exec api python /app/scripts/import_data.py /app/data/clan_sample_data.csv
```

### Step 3: Access the API

- **API Base URL**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Stop Services

```bash
docker-compose down
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/clans/` | Create a new clan |
| GET | `/clans/` | List all clans |
| GET | `/clans/search?name=xxx` | Search clans by name (min 3 chars) |
| DELETE | `/clans/{id}` | Delete a clan by UUID |

## API Examples

### Create a Clan

```bash
curl -X POST http://localhost:8000/clans/ \
  -H "Content-Type: application/json" \
  -d '{"name": "MyNewClan", "region": "TR"}'
```

Response:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "MyNewClan",
  "region": "TR",
  "created_at": "2025-12-28T10:30:00"
}
```

### List All Clans

```bash
curl http://localhost:8000/clans/
```

### Search Clans by Name

```bash
curl "http://localhost:8000/clans/search?name=shadow"
```

Response:
```json
[
  {
    "id": "c9dd7700-5936-481c-a310-93f3f41beb22",
    "name": "ShadowReavers",
    "region": "JP",
    "created_at": "2024-07-19T01:44:33"
  }
]
```

### Delete a Clan

```bash
curl -X DELETE http://localhost:8000/clans/550e8400-e29b-41d4-a716-446655440000
```

## Database Schema

```sql
CREATE TABLE clans (
    id CHAR(36) PRIMARY KEY,        -- UUID
    name VARCHAR(255) NOT NULL,
    region VARCHAR(10) NOT NULL,
    created_at DATETIME NOT NULL    -- UTC timezone
);
CREATE INDEX idx_clans_name ON clans(name);
```

## Running Without Docker (Local Python)

If you prefer to run without Docker:

### Prerequisites

- Python 3.9+
- MySQL 8.0 running locally

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "DATABASE_URL=mysql+pymysql://root:password@localhost:3306/clans_db" > .env

# Create database
mysql -u root -p -e "CREATE DATABASE clans_db;"

# Run the API
uvicorn app.main:app --reload --port 8000

# Import sample data (in another terminal)
python scripts/import_data.py data/clan_sample_data.csv
```

## Cloud Deployment (Google Cloud Run)

For production deployment on Google Cloud:

### Prerequisites

- Google Cloud account with billing enabled
- `gcloud` CLI installed and authenticated

### Step 1: Create Cloud SQL Instance

1. Go to Google Cloud Console → SQL
2. Create a MySQL 8.0 instance
3. Create a database (e.g., `clans_db`)
4. Create a user with password
5. Note the connection name: `PROJECT_ID:REGION:INSTANCE_NAME`

### Step 2: Enable Required APIs

```bash
gcloud services enable cloudbuild.googleapis.com run.googleapis.com sqladmin.googleapis.com
```

### Step 3: Deploy to Cloud Run

```bash
gcloud run deploy clans-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --add-cloudsql-instances=PROJECT_ID:REGION:INSTANCE_NAME \
  --set-env-vars="DATABASE_URL=mysql+pymysql://USER:PASSWORD@/DATABASE?unix_socket=/cloudsql/PROJECT_ID:REGION:INSTANCE_NAME"
```

### Step 4: Import Data to Cloud SQL

```bash
# Authenticate for Cloud SQL Proxy
gcloud auth application-default login

# Download and run Cloud SQL Proxy
curl -o cloud-sql-proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.14.0/cloud-sql-proxy.darwin.arm64
chmod +x cloud-sql-proxy
./cloud-sql-proxy PROJECT_ID:REGION:INSTANCE_NAME --port 3306

# In another terminal, run import
DATABASE_URL="mysql+pymysql://USER:PASSWORD@127.0.0.1:3306/DATABASE" python scripts/import_data.py data/clan_sample_data.csv
```

## Methodology & Assumptions

### Architecture Decisions

1. **Layered Architecture**: Clean separation of concerns:
   - `routers/` - HTTP request handling and validation
   - `services/` - Business logic
   - `models/` - Database ORM models
   - `schemas/` - Request/response data validation

2. **UUID Primary Keys**: Using UUIDs (stored as CHAR(36)) for globally unique identifiers, making future data migrations and distributed systems easier to handle.

3. **UTC Timestamps**: All timestamps are stored in UTC timezone for consistency across different regions.

4. **Connection Pooling**: Configured with `pool_pre_ping=True` and `pool_recycle=300` to handle connection drops gracefully.

### Assumptions

- Clan names are case-insensitive for search operations
- Region codes are stored as-is (no strict validation on import)
- Empty names in CSV are skipped during import
- Unix timestamps in CSV are converted to UTC datetime

### Data Cleaning (CSV Import)

The import script handles the following data quality issues:
- Empty `created_at` values → Uses current UTC time
- Unix timestamp format → Converts to datetime
- Empty `name` values → Skips the row
- Invalid data → Logs and continues with valid records

### API Screenshots

#### All API Endpoints
![All Endpoints](screenshots/all_end_points.png)

#### Health Check
![Health Check](screenshots/health_check.png)

#### List All Clans
![List Clans](screenshots/list_clans.png)

#### Search Clans
![Search Clans](screenshots/search_clans.png)

#### Create Clan
![Create Clan](screenshots/create_clan.png)

#### Delete Clan
![Delete Clan](screenshots/delete_clan.png)

---

## Part 2: Data Analytics & Visualization

### Overview

Processed ~7.3 million rows of user daily metrics data using DBT and BigQuery, then built an interactive dashboard in Looker Studio.

### Technology Stack

- **Data Warehouse**: Google BigQuery
- **Transformation**: DBT (Data Build Tool)
- **Visualization**: Looker Studio

### Data Pipeline

```
Raw CSV Data (17 files, ~7.3M rows)
         │
         ▼
    BigQuery (raw)
         │
         ▼ DBT (cleaning & aggregation)
         │
    BigQuery (daily_metrics table, ~11.4k rows)
         │
         ▼
    Looker Studio Dashboard
```

### Data Cleaning

The DBT models handle the following data quality issues:
- NULL/empty platform values → Converted to 'UNKNOWN'
- Empty country values → Converted to 'Unknown'
- NULL numeric values (revenue, counts) → Converted to 0
- Standardized platform names to uppercase (ANDROID/IOS)

### Output Metrics

The `daily_metrics` model aggregates data by date, country, and platform:

| Metric | Description |
|--------|-------------|
| DAU | Daily Active Users |
| Total IAP Revenue | Sum of in-app purchase revenue |
| Total Ad Revenue | Sum of advertisement revenue |
| ARPDAU | Average Revenue Per Daily Active User |
| Matches Started | Total matches started |
| Win Ratio | Victories / Total matches ended |
| Server Error per DAU | Connection errors per user |

### Key Findings

| Metric | Value |
|--------|-------|
| Total User-Days | 7.29M |
| Unique Users | 2.45M |
| Date Range | Feb 15 - Mar 15, 2024 (30 days) |
| Countries | 233 |

| Platform | User-Days | Total Revenue | Avg ARPDAU |
|----------|-----------|---------------|------------|
| Android | 4.77M | $470,654 | $0.117 |
| iOS | 2.53M | $609,297 | $0.180 |

### Dashboard Screenshots

#### Dashboard Overview
![Dashboard Overview](screenshots/dashboard_overview.png)

#### DAU Trend
![DAU Trend](screenshots/dau_trend.png)

#### Revenue Over Time
![Revenue Over Time](screenshots/revenue_over_time.png)

#### Platform Comparison
![Platform Comparison](screenshots/platform_comparison.png)

---

## License

This project was created as a case study for Vertigo Games.
