import sqlite3
from datetime import datetime


def db_conn():
    """ SQLite database connection and cursor  """
    conn = sqlite3.connect('./wp.db')
    cur = conn.cursor()

    return conn, cur


def build_tables():
    """ Build db tables if they dont already exist  """
    conn, cur = db_conn()
    try:
        with conn:
            cur.execute("""CREATE TABLE IF NOT EXISTS past_workouts (link TEXT PRIMARY KEY, workout_date TEXT)""")
            cur.execute("""CREATE TABLE IF NOT EXISTS user_details (username TEXT PRIMARY KEY, passwordhash TEXT, salt TEXT, website TEXT)""")
    finally:
        conn.close()


def check_workout(td_link):
    """ Check if workout has been already been loaded on the same day """
    conn, cur = db_conn()
    try:
        if cur.execute("SELECT 1 FROM past_workouts WHERE link=? AND strftime('%Y-%m-%d', workout_date) = ?", (td_link, get_now())).fetchone():
            return True
    finally:
        conn.close()


def load_workout(td_link):
    """ Function to load workout link into database """
    conn, cur = db_conn()
    try:
        with conn:
            cur.execute("INSERT INTO past_workouts VALUES(?,?)", (td_link, get_now()))
    finally:
        conn.close()


def get_last_workout():
    """ Returns the last workout loaded into the wp database """
    #NOTE: not in use
    conn, cur = db_conn()
    try:
        result = cur.execute("""SELECT link FROM past_workouts ORDER BY workout_date DESC LIMIT 1 """).fetchone()
        return result
    finally:
        conn.close()


def get_now():
    """ returns todays date in YYYY-MM-DD """
    return datetime.now().strftime('%Y-%m-%d')