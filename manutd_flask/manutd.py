from icalendar import Calendar, Event, vCalAddress, vText
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
import wget
import os
import psycopg2, json
from hvac_lib import HVACClient

app = Flask(__name__)

def get_db_connection():
    with open ("db_conn.json", "r") as file:
        data =json.load(file)
    try:
        conn = psycopg2.connect(
            host=data["host"],
            port=data["port"],
            database="postgres",
            user=data["user"],
            password=data["password"]
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
        if data:
            game_string = f"[{data[4]}] -- {data[1]} V {data[2]} at {data[3]} | {str(data[5])} | {str(data[6])}"
            return game_string
        else:
            return "No upcoming games found."
    else:
        return "Database connection failed."

@app.route('/remaining', methods=['GET'])
def remaining_game():
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

        return jsonify(games)
    else:
        return "Database connection failed."

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
                    cst_localtime = (datetime_obj - timedelta(hours=6))
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

def main():
    conn = get_db_connection()
    populateDB(conn)

if __name__ == '__main__':
    main()
    app.run(debug=True, host="0.0.0.0", port=5000)