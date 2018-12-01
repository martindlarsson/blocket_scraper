import sqlite3
from sqlite3 import Error
import datetime



sql_create_log_table = """ CREATE TABLE IF NOT EXISTS logg (
                                        tid datetime NOT NULL,
                                        meddelande text NOT NULL
                                    ); """

# TODO clean old log entries


def create_connection():
    try:
        db_file = "logg.db"
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def run_sql(conn, script):
    try:
        c = conn.cursor()
        c.execute(script)
    except Error as e:
        print("(Logger) Error running SQL script: " + str(e))


def save(message):
    try:
        print(message)

        sql = ''' INSERT INTO logg(tid,meddelande) VALUES(?,?) '''

        conn = create_connection() #self.__shared_state["conn"]

        if conn is not None:
            cur = conn.cursor()
            cur.execute(sql, (str(datetime.datetime.now()), message))
            conn.commit()
        else:
            print("(Logger) Error! cannot create the database connection.")

    except Exception as exc:
        print("(Logger) Error! Exception: " + str(exc))

    finally:
        if conn is not None:
            conn.close()