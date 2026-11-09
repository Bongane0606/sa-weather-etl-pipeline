"""Read-only API for the existing weather_data PostgreSQL table."""
import os
from datetime import datetime, date
from decimal import Decimal
from flask import Flask, jsonify, request, send_from_directory
from psycopg2 import connect, OperationalError, errors
from psycopg2.extras import RealDictCursor

app = Flask(__name__, static_folder='static')

def connection():
    return connect(host=os.getenv('DB_HOST','localhost'), port=os.getenv('DB_PORT','5432'),
                   dbname=os.getenv('DB_NAME','weather_db'), user=os.getenv('DB_USER','postgres'),
                   password=os.getenv('DB_PASSWORD',''), connect_timeout=4)

def serialize(value):
    if isinstance(value, Decimal): return float(value)
    if isinstance(value, (datetime,date)): return value.isoformat()
    return value

def query(sql, params=()):
    with connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql,params)
            return [{k:serialize(v) for k,v in row.items()} for row in cur.fetchall()]

@app.get('/')
def index():
    return send_from_directory(app.static_folder,'index.html')

@app.get('/api/health')
def health():
    try:
        query('SELECT 1 AS ok')
        return jsonify(status='ok',database='connected')
    except Exception:
        return jsonify(status='degraded',database='unavailable'),503

@app.get('/api/cities')
def cities():
    return jsonify(query('SELECT DISTINCT city, province FROM weather_data ORDER BY city'))

@app.get('/api/summary')
def summary():
    city=request.args.get('city','').strip()
    where='WHERE city = %s' if city else ''
    params=(city,) if city else ()
    return jsonify(query(f"""SELECT COUNT(*) AS total_records, COUNT(DISTINCT city) AS cities,
          ROUND(AVG(temperature_c),2) AS avg_temperature_c,
          ROUND(AVG(humidity_percent),1) AS avg_humidity_percent,
          MAX(extracted_at) AS last_recorded_at FROM weather_data {where}""",params)[0])

@app.get('/api/latest')
def latest():
    city=request.args.get('city','').strip()
    where='WHERE city = %s' if city else ''
    return jsonify(query(f"""SELECT DISTINCT ON (city) id,city,province,country,temperature_c,
      feels_like_c,humidity_percent,wind_speed_mps,condition,extracted_at
      FROM weather_data {where} ORDER BY city,extracted_at DESC,id DESC""", (city,) if city else ()))

@app.get('/api/history')
def history():
    city=request.args.get('city','').strip()
    try: limit=min(max(int(request.args.get('limit',200)),1),1000)
    except ValueError: return jsonify(error='limit must be an integer'),400
    where='WHERE city = %s' if city else ''
    params=(city,limit) if city else (limit,)
    return jsonify(query(f"""SELECT id,city,province,country,temperature_c,feels_like_c,
       temp_min_c,temp_max_c,humidity_percent,wind_speed_mps,condition,extracted_at
       FROM weather_data {where} ORDER BY extracted_at DESC,id DESC LIMIT %s""",params))

@app.errorhandler(OperationalError)
@app.errorhandler(errors.UndefinedTable)
def db_error(error):
    app.logger.warning('Database unavailable or schema missing: %s',type(error).__name__)
    return jsonify(error='Weather database is unavailable or weather_data table has not been created.'),503

if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000)
