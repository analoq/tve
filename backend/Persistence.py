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
            cur.execute("""CREATE TABLE moisture_archive(
                               dt DATETIME,
                               value INT
                           )""")
            cur.execute("""CREATE INDEX idx_moisture_archive_dt
                                     ON moisture_archive(dt DESC)""")
            con.commit()
            con.close()

    def store(self, sample_dt, sample_value):
        """Store a sample's datetime and value"""
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        cur.execute("""INSERT INTO moisture(dt, value)
                       VALUES(?, ?)""",
                    [sample_dt.strftime('%Y-%m-%d %H:%M:%S'), sample_value])
        con.commit()
        con.close()

    @staticmethod
    def _format(resultset):
        result = []
        for row in resultset:
            result.append({
                'dt': datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'),
                'value': row[1]
            })
        return result

    def historical(self, seconds):
        """Return historical data for provided delta, in seconds"""
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        cur.execute("""SELECT dt, value
                       FROM moisture
                       WHERE dt >= datetime('now', '-%d seconds')
                       ORDER BY dt""" % seconds)
        result = self._format(cur)
        con.close()
        return result

    def archive(self):
        """Aggregate older data to archive table"""
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        cur.execute("""SELECT datetime(strftime('%Y-%m-%d %H:00:00', dt), '+'||(strftime('%M', dt)/15*15)||' minutes'),
                              ROUND(AVG(value))
                       FROM moisture
                       WHERE dt < strftime('%Y-%m-%d %H:00:00', 'now')
                       GROUP BY strftime('%Y-%m-%d %H', dt), strftime('%M', dt)/15""")
        result = self._format(cur)
        for row in result:
            cur.execute("""INSERT INTO moisture_archive(dt, value)
                           VALUES(?, ?)""", (row['dt'], row['value']))
        cur.execute("""DELETE FROM moisture
                       WHERE dt < strftime('%Y-%m-%d %H:00:00', 'now')""")
        con.commit()
        con.close()
        return result

    def historical_archive(self, hours):
        """Return archived historical data for provided delta, in hours"""
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        cur.execute("""SELECT dt, value
                       FROM moisture_archive
                       WHERE dt >= datetime('now', '-%d hours')
                       ORDER BY dt""" % hours)
        result = self._format(cur)
        con.close()
        return result

