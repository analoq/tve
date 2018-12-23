"""Persistence module encompasses persistence concerns"""
import os
import sqlite3
from datetime import datetime


class Persistence(object):
    """Persistence class"""
    def __init__(self, db_name):
        """Initialize persistence object with given db_name"""
        self.db_name = db_name
        if not os.path.exists(self.db_name):
            con = sqlite3.connect(self.db_name)
            cur = con.cursor()
            cur.execute("""CREATE TABLE moisture(
                               dt DATETIME,
                               value INT
                           )""")
            cur.execute("""CREATE INDEX idx_moisture_dt
                                     ON moisture(dt DESC)""")
            con.commit()
            con.close()

    def store(self, sample_dt, sample_value):
        """Store a sample's datetime and value"""
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        cur.execute("""INSERT INTO moisture(dt, value)
                       VALUES(?, ?)""", [sample_dt, sample_value])
        con.commit()
        con.close()

    def historical(self, delta):
        """Return historical data for provided delta, in seconds"""
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        cur.execute("""SELECT dt, value
                       FROM moisture
                       WHERE dt >= datetime('now', '-%d seconds')
                       ORDER BY dt""" % delta)
        result = []
        for row in cur:
            result.append({
                'dt': datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f'),
                'value': row[1]
            })
        con.close()
        return result
