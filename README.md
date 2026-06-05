# 🌦️ SA Weather ETL Pipeline

A Python-based ETL (Extract, Transform, Load) pipeline that pulls real-time weather data
for major South African cities using the OpenWeatherMap API, transforms it into a clean
structured format, and stores it in a CSV file for analysis.

---

## 📌 Project Overview

This project demonstrates a foundational data engineering concept — building an automated
data pipeline that moves data from a source (API), transforms it, and loads it into a
destination (CSV / data store).

**Cities tracked:**
- Johannesburg
- Cape Town
- Durban
- Pretoria

---

## 🏗️ Pipeline Architecture
EXTRACT                   TRANSFORM                  LOAD
───────                   ─────────                  ────
OpenWeatherMap API   →    Clean & restructure   →    CSV File
(Raw JSON data)           (Select fields,            (output/weather_data.csv)
format timestamps)

---

## 📁 Project Structure
sa-weather-etl-pipeline/
│
├── weather_etl/
│   ├── extract.py        # Pulls raw data from OpenWeatherMap API
│   ├── transform.py      # Cleans and restructures raw data
│   ├── load.py           # Saves transformed data to CSV
│   └── pipeline.py       # Orchestrates the full ETL pipeline
│
├── output/
│   └── weather_data.csv  # Final output (auto-generated on run)
│
├── .venv/                # Virtual environment (not tracked by Git)
├── .gitignore
└── README.md

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3 | Core programming language |
| Requests | HTTP library for API calls |
| CSV (stdlib) | Writing structured output files |
| OpenWeatherMap API | Real-time weather data source |

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/sa-weather-etl-pipeline.git
cd sa-weather-etl-pipeline
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv .venv

# On Linux/Mac:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install requests
```

### 4. Add your API key
Get a free API key from [OpenWeatherMap](https://openweathermap.org/api),
then open `weather_etl/extract.py` and replace:
```python
API_KEY = "your_api_key_here"
```

### 5. Run the pipeline
```bash
cd weather_etl
python3 pipeline.py
```

---

## 📊 Sample Output
==================================================
SA WEATHER ETL PIPELINE
Started at: 2026-06-05 08:30:00
📡 STEP 1: EXTRACTING data from API...
✅ Successfully extracted data for Johannesburg
✅ Successfully extracted data for Cape Town
✅ Successfully extracted data for Durban
✅ Successfully extracted data for Pretoria
🔧 STEP 2: TRANSFORMING raw data...
✅ Transformed data for Johannesburg
...
💾 STEP 3: LOADING data into CSV...
✅ Loaded data for Johannesburg into CSV
...
==================================================
✅ PIPELINE COMPLETED SUCCESSFULLY

---

## 📈 Data Fields Captured

| Field | Description |
|-------|-------------|
| `city` | City name |
| `country` | Country code (ZA) |
| `temperature_c` | Current temperature in Celsius |
| `feels_like_c` | Feels like temperature in Celsius |
| `temp_min_c` | Minimum temperature |
| `temp_max_c` | Maximum temperature |
| `humidity_percent` | Humidity percentage |
| `wind_speed_mps` | Wind speed in metres per second |
| `condition` | Weather condition (e.g. clear sky) |
| `extracted_at` | Timestamp of when data was collected |

---

## 🚀 Future Improvements

- [ ] Store data in a PostgreSQL database instead of CSV
- [ ] Add Apache Airflow to schedule the pipeline automatically
- [ ] Add data quality checks (missing values, outliers)
- [ ] Visualise the data using a dashboard (Matplotlib / Power BI)
- [ ] Containerise the pipeline using Docker
- [ ] Expand to more South African cities

---

## 👤 Author

**Letsoenyo Clen Bongane**
Aspiring Data Engineer | Currently studying at WeThinkCode_

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://linkedin.com/in/Bongane_Clen)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black)](https://github.com/Bongane0606)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).