from icalendar import Calendar, Event, vCalAddress, vText
from datetime import datetime, timedelta
from hvac_lib import HVACClient
from flask import Flask,  jsonify, request
import wget
import hashlib
import os
import psycopg2

app = Flask(__name__)

@app.route('/', methods = ['GET']) 
def home(): 
    if(request.method == 'GET'):   
        data = "Manchester United Fixtures"
        return data 

@app.route('/next_game', methods = ['GET']) 
def next_game():
    SQLQuery = f"""
    select * from match
    where date > '{today}'
    order by date
    limit 1
    """ 
    conn = psycopg2.connect(db_info)
    cur = conn.cursor()
    cur.execute(SQLQuery)
    data = cur.fetchone()
    cur.close()
    conn.close()
    game_string = f"[{data[4]}] -- {data[1]} V {data[2]} at {data[3]} | {str(data[5])} | {str(data[6])}"
    return game_string

@app.route('/remaining_games', methods = ['GET']) 
def remaining_game():
    SQLQuery = f"""
    select * from match
    where date > '{today}'
    order by date
    """ 
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(SQLQuery)
    all_data = cur.fetchall()
    cur.close()
    conn.close()

    games = []
    for data in all_data:
        string = f"[{data[4]}] -- {data[1]} V {data[2]} at {data[3]} | {str(data[5])} | {str(data[6])}"
        games.append(string)
    
    return games

def downloadICS():
    url = "https://www.skysports.com/calendars/football/fixtures/teams/manchester-united"
    downloadfile = wget.download(url)

def get_db_connection(username, pwd):
    vault_client = HVACClient()
    creds =  vault_client.read('secret/data/postgres')
    for key, value in creds.items():
        username = key
        pwd = value
    
    conn = psycopg2.connect(
        host="localhost",
        database="fixtures",
        user=username,
        password=pwd
    )
    return conn

def populateFixtures():
    matches = []
    with open('manchester-united', 'rb') as ical:
        ecal = Calendar.from_ical(ical.read())
        uid = 1
        for component in ecal.walk():
            if component.name == "VEVENT":
                description = component.decoded("description")
                datetime = component.decoded("dtstart")
                cst_localtime = (datetime - timedelta(hours=6))
                game = description.decode("utf-8").split('-')[0]

                hometeam =  description.decode("utf-8").split('-')[0].split(' v ')[0]
                awayteam = description.decode("utf-8").split('-')[0].split(' v ')[1]
                stadium = description.decode("utf-8").split('-')[1]
                comp = description.decode("utf-8").split('-')[2]
                date = cst_localtime.date()
                time = cst_localtime.time()

                matchinfo = {
                    "UID"           : uid,
                    "home_team"     : hometeam,
                    "away_team"     : awayteam,
                    "stadium"       : stadium,
                    "competition"   : comp,
                    "date"          : str(date),
                    "time"          : str(time)
                }

                matches.append(matchinfo)
                uid =  uid + 1
    
    os.remove('manchester-united')
    return matches

def populateDB(conn):
    downloadICS()
    matches = populateFixtures()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS match (
        uid INT PRIMARY KEY,
        home_team VARCHAR(255),
        away_team VARCHAR(255),
        stadium VARCHAR(255),
        competition VARCHAR(255),
        date DATE,
        time TIME
    );
    """)
    cur.executemany("""
                    INSERT INTO match (uid,home_team,away_team,stadium,competition,date,time)
                    VALUES (%(UID)s,%(home_team)s,%(away_team)s,%(stadium)s,%(competition)s,%(date)s,%(time)s)
                    ON CONFLICT (uid) DO NOTHING;""",
                    data)
    cur.close()
    conn.commit()
    conn.close()

def main():

    conn = get_db_connection()

    # os.environ['POSTGRES_USER'] = username
    # os.environ['POSTGRES_PASSWORD'] = pwd
    # os.environ['POSTGRES_DB'] = 'fixtures'

    populateDB(conn)
    today = datetime.today().strftime('%Y-%m-%d')
    app = Flask(__name__)


if __name__ == '__main__':
    main()
    app.run(debug = True, host="0.0.0.0", port=5000) 


