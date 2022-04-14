import sqlite3


def GetTables(db_file = 'db.sqlite3'):
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("select name from sqlite_master where type='table' order by name")
        print(cur.fetchall())
    except sqlite3.Error as e:
            print(e)


GetTables()