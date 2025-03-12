from flask import Flask,  jsonify, request
import psycopg2
from datetime import datetime

db_info = """
    dbname=fixtures
    user=postgres
    password=postgres
    host=postgres
    port=5432
"""
today = datetime.today().strftime('%Y-%m-%d')
print(today)
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
    conn = psycopg2.connect(db_info)
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
    

if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0", port=5000) 
