from icalendar import Calendar, Event, vCalAddress, vText
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
import wget
import os
import psycopg2, json
from hvac_lib import HVACClient
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit
from prometheus_client import generate_latest, Counter, Histogram, Summary
from prometheus_client import CONTENT_TYPE_LATEST
import time



app = Flask(__name__)

# Track number of HTTP requests by method and endpoint
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method'])
# Track request latency in seconds
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP Request Latency')

def get_secret():
    client = HVACClient()
    creds = client.read('secret/data/postgres')
    for k,v in creds.items():
        uname = k
        pwd = v
    return uname, pwd

def get_db_connection():
    uname, pwrd = get_secret()

    try:
        conn = psycopg2.connect(
            host="192.168.68.86",
            port=32262,
            database="postgres",
            user=uname,
            password=pwrd
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

@app.route('/', methods=['GET'])
def home():
    if request.method == 'GET':
        data = "Manchester United Fixtures"
        return data

@app.route('/next', methods=['GET'])
def next_game():
    start_time = time.time()
    REQUEST_COUNT.labels(method='GET').inc()

    today = datetime.today().strftime('%Y-%m-%d')
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        SQLQuery = f"""
            SELECT * FROM match
            WHERE date > '{today}'
            ORDER BY date
            LIMIT 1
        """
        cur.execute(SQLQuery)
        data = cur.fetchone()
        cur.close()
        conn.close()

        duration = time.time() - start_time
        REQUEST_LATENCY.observe(duration)

        if data:
            game_string = f"[{data[4]}] -- {data[1]} V {data[2]} at {data[3]} | {str(data[5])} | {str(data[6])}"
            return game_string
        else:
            return "No upcoming games found."
    else:
        return "Database connection failed."

@app.route('/remaining', methods=['GET'])
def remaining_game():
    start_time = time.time()
    REQUEST_COUNT.labels(method='GET').inc()

    today = datetime.today().strftime('%Y-%m-%d')
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        SQLQuery = f"""
            SELECT * FROM match
            WHERE date > '{today}'
            ORDER BY date
        """
        cur.execute(SQLQuery)
        all_data = cur.fetchall()
        cur.close()
        conn.close()

        games = []
        for data in all_data:
            string = f"[{data[4]}] -- {data[1]} V {data[2]} at {data[3]} | {str(data[5])} | {str(data[6])}"
            games.append(string)

        duration = time.time() - start_time
        REQUEST_LATENCY.observe(duration)

        return jsonify(games)
    else:
        return "Database connection failed."

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

def downloadICS():
    url = "https://www.skysports.com/calendars/football/fixtures/teams/manchester-united"
    try:
        downloadfile = wget.download(url, out='manchester-united')
        return True
    except Exception as e:
        print(f"Error downloading ICS file: {e}")
        return False

def populateFixtures():
    matches = []
    try:
        with open('manchester-united', 'rb') as ical:
            ecal = Calendar.from_ical(ical.read())
            uid = 1
            for component in ecal.walk():
                if component.name == "VEVENT":
                    description = component.decoded("description")
                    datetime_obj = component.decoded("dtstart")
                    cst_localtime = (datetime_obj - timedelta(hours=5))
                    game = description.decode("utf-8").split('-')[0]

                    hometeam = description.decode("utf-8").split('-')[0].split(' v ')[0].strip()
                    awayteam = description.decode("utf-8").split('-')[0].split(' v ')[1].strip()
                    stadium = description.decode("utf-8").split('-')[1].strip()
                    comp = description.decode("utf-8").split('-')[2].strip()
                    date = cst_localtime.date()
                    time = cst_localtime.time()

                    matchinfo = {
                        "UID": uid,
                        "home_team": hometeam,
                        "away_team": awayteam,
                        "stadium": stadium,
                        "competition": comp,
                        "date": str(date),
                        "time": str(time)
                    }

                    matches.append(matchinfo)
                    uid += 1

        os.remove('manchester-united')
        return matches
    except FileNotFoundError:
        print("ICS file not found.")
        return []

def populateDB(conn):
    if downloadICS():
        matches = populateFixtures()
        if conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS match (
                uid INT PRIMARY KEY,
                home_team VARCHAR(255),
                away_team VARCHAR(255),
                stadium VARCHAR(255),
                competition VARCHAR(255),
                date DATE,
                time TIME
                );
            """)
            if matches:
                 cur.executemany("""
                    INSERT INTO match (uid, home_team, away_team, stadium, competition, date, time)
                    VALUES (%(UID)s, %(home_team)s, %(away_team)s, %(stadium)s, %(competition)s, %(date)s, %(time)s)
                    ON CONFLICT (uid) DO NOTHING;
                """, matches)
            cur.close()
            conn.commit()
            conn.close()
        else:
            print("Database connection failed.")

def schedule_weekly_update():
    scheduler = BackgroundScheduler()
    scheduler.start()

    # Run once a week
    scheduler.add_job(
        func=lambda: populateDB(get_db_connection()),
        trigger=IntervalTrigger(weeks=1),
        id='weekly_db_update',
        name='Update match fixtures every week',
        replace_existing=True
    )

    # Shutdown scheduler when app exits
    atexit.register(lambda: scheduler.shutdown())

def main():
    conn = get_db_connection()
    populateDB(conn)
    schedule_weekly_update()

if __name__ == '__main__':
    main()
    app.run(debug=True, host="0.0.0.0", port=6000)