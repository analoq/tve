"""Persistence module encompasses persistence concerns"""
import os
import sqlite3
from datetime import datetime


class Persistence(object):
    """Persistence class"""
    def __init__(self, db_name):
        """Initialize persistence object with given db_name"""
        self.db_name = db_name
        sqlite3.register_adapter(datetime, Persistence.adapt_datetime)
        sqlite3.register_converter('datetime', Persistence.convert_datetime)
        if not os.path.exists(self.db_name):
            con = sqlite3.connect(self.db_name)
            cur = con.cursor()
            cur.execute("""CREATE TABLE sample(
                               dt DATETIME,
                               moisture REAL,
                               luminence REAL,
                               temperature REAL,
                               humidity REAL
                           )""")
            cur.execute("""CREATE INDEX idx_sample_dt
                                     ON sample(dt DESC)""")
            cur.execute("""CREATE TABLE sample_archive(
                               dt DATETIME,
                               moisture REAL,
                               luminence REAL,
                               temperature REAL,
                               humidity REAL
                           )""")
            cur.execute("""CREATE INDEX idx_sample_archive_dt
                                     ON sample_archive(dt DESC)""")
            con.commit()
            con.close()

    @staticmethod
    def convert_datetime(s):
        return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')

    @staticmethod
    def adapt_datetime(dt):
        return dt.strftime('%Y-%m-%d %H:%M:%S')
        
    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def _connection(self):
        con = sqlite3.connect(
                database=self.db_name,
                detect_types=sqlite3.PARSE_DECLTYPES
            )
        con.row_factory = self.dict_factory
        return con

    def store(self, sample_dt, moisture, luminence, temperature, humidity):
        """Store a sample's datetime and value"""
        con = self._connection()
        cur = con.cursor()
        cur.execute("""INSERT INTO sample(dt, moisture, luminence, temperature, humidity)
                       VALUES(?, ?, ?, ?, ?)""",
                    [sample_dt, moisture, luminence, temperature, humidity])
        con.commit()
        con.close()

    def historical(self, seconds):
        """Return historical data for provided delta, in seconds"""
        con = self._connection()
        cur = con.cursor()
        cur.execute("""SELECT dt, moisture, luminence, temperature, humidity
                       FROM sample
                       WHERE dt >= datetime('now', '-%d seconds')
                       ORDER BY dt""" % seconds)
        result = cur.fetchall()
        con.close()
        return result

    def archive(self):
        """Aggregate older data to archive table"""
        con = self._connection()
        cur = con.cursor()

        cur.execute("""INSERT INTO sample_archive(dt, moisture, luminence, temperature, humidity)
                       SELECT strftime('%Y-%m-%d %H:00:00', dt),
                              AVG(moisture), AVG(luminence), AVG(temperature), AVG(humidity)
                       FROM sample
                       WHERE dt < strftime('%Y-%m-%d %H:00:00', 'now')
                       GROUP BY strftime('%Y-%m-%d %H', dt)""")
        cur.execute("""DELETE FROM sample
                       WHERE dt < strftime('%Y-%m-%d %H:00:00', 'now')""")
        con.commit()
        con.close()

    def historical_archive(self, hours):
        """Return archived historical data for provided delta, in hours"""
        con = self._connection()
        cur = con.cursor()
        cur.execute("""SELECT dt, moisture, luminence, temperature, humidity
                       FROM sample_archive
                       WHERE dt >= datetime('now', '-%d hours')
                       ORDER BY dt""" % hours)
        result = cur.fetchall()
        con.close()
        return result

