# SA Weather Analytics Dashboard

This adds a **read-only Flask API** and responsive HTML/CSS/JavaScript dashboard to the original project. Your ETL, Airflow, PostgreSQL database and original `dashboard.html` remain intact.

## Start with Docker (Pop!_OS / Linux)

1. Open a terminal in the extracted project directory.
2. Keep your existing `.env` file, or create one with `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_PORT`, and `API_KEY` (see original README). **Do not commit `.env`.**
3. Run:

```bash
docker compose up -d --build postgres dashboard
docker compose ps
docker compose logs -f dashboard
```

4. Open **http://localhost:5050**. The API is at `/api/health`, `/api/cities`, `/api/summary`, `/api/latest`, and `/api/history?city=Johannesburg&limit=100`.
5. If the database is empty, run your existing pipeline (requires a valid OpenWeatherMap API key):

```bash
docker compose run --rm app python weather_etl/pipeline.py
```

Check your existing Dockerfile/README for the exact pipeline command if its working directory differs. The dashboard does **not** import CSV data automatically; it reads PostgreSQL only.

## Airflow (optional)

```bash
docker compose up -d --build airflow-init airflow-webserver airflow-scheduler
```

Airflow is available at **http://localhost:8080** once initialized. The dashboard's API does not claim to monitor Airflow run status; it reports observation timestamps from PostgreSQL.

## Run API without Docker (optional)

```bash
python3 -m venv .dashboard-venv
source .dashboard-venv/bin/activate
pip install -r dashboard_api/requirements.txt
# Export DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD or use an env loader.
cd dashboard_api
python app.py
```

Local Flask development listens on **http://localhost:5000**. The production Docker service uses Gunicorn and port **5050** on the host.

## API endpoints

- `GET /api/health` checks the database connection.
- `GET /api/cities` lists unique cities and provinces.
- `GET /api/summary?city=...` returns counts, averages, latest observation timestamp.
- `GET /api/latest?city=...` returns the most recent observation per city.
- `GET /api/history?city=...&limit=200` returns up to 1000 recent observations.

All endpoints are read-only. Database credentials are passed through environment variables, never exposed to the browser. Weather observations are **historical**, not a live forecast.

## Troubleshooting

- Empty dashboard: run the pipeline to populate `weather_data` and check `docker compose logs app`.
- `weather_data` missing: initialize the table through the existing pipeline/db setup.
- Port 5050 in use: change `5050:5000` in `docker-compose.yml` to `5051:5000`.
- Chart not visible: Chart.js is loaded from a CDN, so internet access is required for the chart; API, cards and table still work without it.
- Database unavailable: `docker compose ps` and `docker compose logs postgres dashboard`.
