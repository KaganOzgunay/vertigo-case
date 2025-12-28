# Clans Management API

A REST API for managing game clans, built with FastAPI and MySQL, deployed on Google Cloud Run.

## Technology Stack

- **Framework**: Python 3.11 + FastAPI
- **Database**: MySQL 8.0 (Cloud SQL in production)
- **ORM**: SQLAlchemy 2.0
- **Containerization**: Docker
- **Deployment**: Google Cloud Run

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
│   └── clan_sample_data.csv # Sample data
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Python 3.11+ (for local development without Docker)

### Run with Docker

```bash
# Start the API and MySQL database
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

The API will be available at: http://localhost:8000

### Import Sample Data

After starting the services:

```bash
# Using Docker
docker-compose exec api python /app/scripts/import_data.py /app/data/clan_sample_data.csv

# Or locally (requires MySQL running)
python scripts/import_data.py
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/clans` | Create a new clan |
| GET | `/clans` | List all clans |
| GET | `/clans/search?name=xxx` | Search clans by name (min 3 chars) |
| DELETE | `/clans/{id}` | Delete a clan by UUID |

### API Documentation

Interactive API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Examples

### Create a Clan

```bash
curl -X POST http://localhost:8000/clans \
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
curl http://localhost:8000/clans
```

### Search Clans

```bash
curl "http://localhost:8000/clans/search?name=shadow"
```

### Delete a Clan

```bash
curl -X DELETE http://localhost:8000/clans/550e8400-e29b-41d4-a716-446655440000
```

## Database Schema

```sql
CREATE TABLE clans (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    region VARCHAR(10) NOT NULL,
    created_at DATETIME NOT NULL
);
```

## Methodology & Assumptions

### Architecture Decisions

1. **Layered Architecture**: The application follows a clean separation of concerns:
   - `routers/` - HTTP request handling and validation
   - `services/` - Business logic
   - `models/` - Database ORM models
   - `schemas/` - Request/response data validation

2. **UUID Primary Keys**: Using UUIDs (stored as CHAR(36)) for globally unique identifiers, making future data migrations and distributed systems easier to handle.

3. **UTC Timestamps**: All timestamps are stored in UTC timezone for consistency across different regions.

4. **Connection Pooling**: Configured with `pool_pre_ping=True` and `pool_recycle=300` to handle Cloud Run cold starts gracefully.

### Assumptions

- Clan names are case-insensitive for search operations
- Region codes are stored as-is (no strict validation on import)
- Empty names in CSV are skipped during import
- Unix timestamps in CSV are converted to UTC datetime

### Data Cleaning (CSV Import)

The import script handles the following data quality issues:
- Empty `created_at` values: Uses current UTC time
- Unix timestamp format: Converts to datetime
- Empty `name` values: Skips the row
- Invalid data: Logs and continues with valid records

## Cloud Deployment

### Google Cloud SQL Setup

1. Create a Cloud SQL MySQL instance
2. Create a database named `clans_db`
3. Create a user with appropriate permissions
4. Note the connection name: `PROJECT_ID:REGION:INSTANCE_NAME`

### Deploy to Cloud Run

```bash
# Authenticate with Google Cloud
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Build and push the container image
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/clans-api

# Deploy to Cloud Run
gcloud run deploy clans-api \
  --image gcr.io/YOUR_PROJECT_ID/clans-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --add-cloudsql-instances=YOUR_PROJECT_ID:us-central1:YOUR_INSTANCE \
  --set-env-vars="DATABASE_URL=mysql+pymysql://USER:PASSWORD@/clans_db?unix_socket=/cloudsql/YOUR_PROJECT_ID:us-central1:YOUR_INSTANCE"
```

## Screenshots

*Screenshots will be added after deployment*

## License

This project was created as a case study.
