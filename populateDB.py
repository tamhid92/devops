from icalendar import Calendar, Event, vCalAddress, vText
from datetime import datetime
from datetime import timedelta
import pymongo
import wget
import uuid
import hashlib
import os

def downloadICS():
    url = "https://www.skysports.com/calendars/football/fixtures/teams/manchester-united"
    downloadfile = wget.download(url)

def createUUID(unistr):
    hex_string = hashlib.md5(unistr.encode("UTF-8")).hexdigest()
    return str(uuid.UUID(hex=hex_string))

def populateFixtures():
    matches = []
    with open('manchester-united', 'rb') as ical:
        ecal = Calendar.from_ical(ical.read())
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

                uuidstring = f"{hometeam}{awayteam}{str(date).replace('-','')}".replace(' ','')
                uid = createUUID(uuidstring)

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
    return matches


def main():
    downloadICS()
    matches = populateFixtures()
    for match in matches:
        with open("fixture.txt", "a+") as outfile:
            print(match, file=outfile)
    
    if os.path.exists("manchester-united"):
        os.remove("manchester-united")
    else:
        print("The file does not exist")

if __name__ == "__main__":
    main()