from icalendar import Calendar, Event, vCalAddress, vText
from datetime import datetime
from datetime import timedelta
# import pymongo
import wget
import uuid
import hashlib
import os
import psycopg2

def downloadICS():
    url = "https://www.skysports.com/calendars/football/fixtures/teams/manchester-united"
    downloadfile = wget.download(url)

# def createUUID(unistr):
#     hex_string = hashlib.md5(unistr.encodecle"UTF-8")).hexdigest()
#     return str(uuid.UUID(hex=hex_string))

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
    return matches

def populateDB(data):
    conn = psycopg2.connect(
        dbname="fixtures",
        user="postgres",
        password="postgres",
        host="postgres",
        port=5431
    )
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
    downloadICS()
    print("Downloaded ICS file")
    matches = populateFixtures()
    print("Scraped ICS file successfully")
    populateDB(matches)
    os.remove('manchester-united')

if __name__ == "__main__":
    main()