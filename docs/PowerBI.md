# 📊 Power BI Dashboard — Setup Guide

This guide takes you from your pipeline's output straight to a working Power BI report. It's written so you can copy/paste each block directly into Power BI Desktop — there's no manual re-typing of queries or measures needed.

> **Why a guide instead of a `.pbix` file:** Power BI's report file is a proprietary binary format that only Power BI Desktop's GUI can reliably write. Everything *content*-related — the query, the model, the measures, the layout — is below and ready to paste in.

---

## 1. Connect to your data

You have two sources already producing the same shape of data — pick whichever fits how you're running the pipeline.

<details open>
<summary><strong>Option A — Connect directly to PostgreSQL (recommended, live data)</strong></summary>

1. Power BI Desktop → **Get Data** → **PostgreSQL database**
2. Server: `localhost` (or `postgres` if Power BI itself is containerized — usually not, so use `localhost` with the port mapped from `docker-compose.yml`)
3. Database: your `DB_NAME` value from `.env`
4. Under **Data Connectivity mode**, choose **Import** (simplest) or **DirectQuery** (always-live, but limits some DAX features)
5. Credentials: your `DB_USER` / `DB_PASSWORD`
6. Select the `weather_data` table and load

</details>

<details>
<summary><strong>Option B — Connect to the CSV output</strong></summary>

1. Power BI Desktop → **Get Data** → **Text/CSV**
2. Point it at `output/weather_data.csv`
3. Note: this file has no header row on older runs (rows were appended before headers existed) — the Power Query step below handles renaming columns manually so this doesn't matter.

</details>

---

## 2. Power Query (M) — cleanup steps

Paste this into **Home → Advanced Editor** (adjust the `Source` line if you used the CSV route):

```m
let
    Source = PostgreSQL.Database("localhost", "weather"),
    weather_data = Source{[Schema="public",Item="weather_data"]}[Data],

    // Ensure correct types (guards against text-typed columns from CSV imports)
    #"Changed Type" = Table.TransformColumnTypes(weather_data, {
        {"city", type text}, {"province", type text}, {"country", type text},
        {"temperature_c", type number}, {"feels_like_c", type number},
        {"temp_min_c", type number}, {"temp_max_c", type number},
        {"humidity_percent", Int64.Type}, {"wind_speed_mps", type number},
        {"condition", type text}, {"extracted_at", type datetime}
    }),

    // Split extracted_at into Date and Time so it plays nicely with a date table
    #"Added Date" = Table.AddColumn(#"Changed Type", "extracted_date", each DateTime.Date([extracted_at]), type date),
    #"Added Hour" = Table.AddColumn(#"Added Date", "extracted_hour", each Time.Hour([extracted_at]), Int64.Type),

    // Title-case the weather condition for consistent display (API sometimes returns lowercase)
    #"Cleaned Condition" = Table.TransformColumns(#"Added Hour", {{"condition", Text.Proper, type text}})
in
    #"Cleaned Condition"
```

**Also add a Date table** (Modeling → New Table) for time intelligence:
```dax
DateTable = CALENDAR(MIN(weather_data[extracted_date]), MAX(weather_data[extracted_date]))
```
Then mark it as a **Date Table** (Table tools → Mark as Date Table) and relate `DateTable[Date] → weather_data[extracted_date]`.

---

## 3. DAX measures

Create these under a `_Measures` table (New Table → `_Measures = {}` as a placeholder, then add measures to it) so they're not scattered across your data table.

```dax
Avg Temperature (°C) =
AVERAGE(weather_data[temperature_c])

Avg Humidity (%) =
AVERAGE(weather_data[humidity_percent])

Avg Wind Speed (m/s) =
AVERAGE(weather_data[wind_speed_mps])

Hottest Province =
CALCULATE(
    SELECTEDVALUE(weather_data[province]),
    TOPN(1, weather_data, weather_data[temperature_c], DESC)
)

Latest Reading Time =
MAX(weather_data[extracted_at])

Records Loaded =
COUNTROWS(weather_data)

Temp vs Provincial Avg =
VAR ProvinceAvg =
    CALCULATE(
        AVERAGE(weather_data[temperature_c]),
        ALLEXCEPT(weather_data, weather_data[province])
    )
RETURN
    AVERAGE(weather_data[temperature_c]) - ProvinceAvg

Rainy Readings % =
DIVIDE(
    CALCULATE(COUNTROWS(weather_data), weather_data[condition] IN {"Light Rain", "Moderate Rain", "Heavy Intensity Rain", "Rain"}),
    COUNTROWS(weather_data)
)
```

---

## 4. Recommended report layout

A single page works well for 9 provinces:

| Zone | Visual | Fields |
|---|---|---|
| Top strip | 4 **Cards** | `Avg Temperature`, `Avg Humidity`, `Hottest Province`, `Latest Reading Time` |
| Left, large | **Shape map** or **ArcGIS map** of South Africa | `province` on location, `Avg Temperature` on color saturation |
| Right, top | **Line chart** | `extracted_at` (x-axis) vs `temperature_c` (y-axis), split by `province` (legend) |
| Right, bottom | **Bar chart** | `province` (x-axis) vs `Avg Wind Speed`/`Avg Humidity` (y-axis) |
| Bottom | **Matrix table** | Rows: `province`, `city`; Values: `Avg Temperature`, `Avg Humidity`, `condition` (last value) |
| Slicer | **Date slicer** | `DateTable[Date]`, and a `condition` slicer for filtering by weather type |

> South Africa isn't in Power BI's built-in Shape Map gallery by default — import a South Africa provinces **TopoJSON/GeoJSON** (searchable on sites like `github.com/deldersveld/topojson`) via Shape Map → Format → Map settings → Add map.

---

## 5. Keeping it live

- **Import mode + PostgreSQL:** Power BI Desktop → **Refresh** re-pulls the latest rows your Airflow-scheduled pipeline has loaded.
- **Publish to Power BI Service:** File → Publish, then set up a **scheduled refresh** (needs an On-premises Data Gateway if Postgres isn't cloud-hosted) matching your Airflow cadence (every 6 hours).
- **DirectQuery mode:** no refresh needed — every visual queries Postgres live, at the cost of some DAX limitations (e.g. some time-intelligence functions).

---

## 6. Once it's built

Update the `README.md` checklist:
```md
- [x] Dashboard using Power BI
```
and consider dropping a screenshot of the finished report into a `docs/` or `screenshots/` folder, linked from the README, since a `.pbix` file itself doesn't render on GitHub.