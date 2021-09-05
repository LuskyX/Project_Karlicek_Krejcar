import sqlite3
from sqlite3 import Error
from config import DB_FILE
from tools.data_classes import VaccCenter


class DatabaseConnector:
    """
    class for working with sqlite3 database
    """
    db_file = DB_FILE

    def __init__(self, update: bool = False):
        self.conn = None
        try:
            self.conn = sqlite3.connect(self.db_file)
        except Error as e:
            print(e)
        self.cur = self.conn.cursor()
        if update:
            self._drop_tables()
            self._create_tables()

    def insert_vacc_center(self, center: VaccCenter):
        """
        for given VaccCenter it insert all information to database
        """
        self._insert_into_vacc_center(center.vacc_id, center.name, center.region, center.link)
        self._insert_into_vacc_center_type(center.vacc_id, center.center_type)
        self._insert_into_vacc_center_vaccines(center.vacc_id, center.vaccines)
        self._insert_into_vacc_center_hours(center.vacc_id, center.open_hours)
        self._insert_into_vacc_center_location(center.vacc_id, center.gps)
        self._insert_into_vacc_center_info(center.vacc_id, center.info)

    def insert_into_locations(self, name: str, gps: tuple):
        """
        insert data into locations table
        """
        query = """
            INSERT INTO locations (name, latitude, longitude)
            VALUES (?, ?, ?);
            """
        self.cur.execute(query, (name, gps[0], gps[1]))
        self.conn.commit()

    def get_data(self, query: str):
        """
        simple method for extracting data
        """
        self.cur.execute(query)
        data = self.cur.fetchall()
        return data

    def _insert_into_vacc_center(self, vacc_id: str, name: str, region: str, link: str):
        """
        insert main info into vacc_center table
        """
        query = """
            INSERT INTO vacc_center (vacc_id, name, region, link)
            VALUES (?, ?, ?, ?);
            """
        self.cur.execute(query, (vacc_id, name, region, link))
        self.conn.commit()

    def _insert_into_vacc_center_type(self, vacc_id: str, center_type: dict):
        """
        insert center_type data into vacc_center_type table
        """
        query = """
            INSERT INTO vacc_center_type (vacc_id, adult, teenage, child, without_registration, self_payers)
            VALUES (?, ?, ?, ?, ?, ?);
            """
        self.cur.execute(query, (vacc_id, center_type['adult'], center_type['teenage'], center_type['child'],
                                 center_type['without_registration'], center_type['self_payers']))
        self.conn.commit()

    def _insert_into_vacc_center_vaccines(self, vacc_id: str, vaccines: dict):
        """
        insert data about vaccines into table vacc_center_vaccines
        """
        query = """
            INSERT INTO vacc_center_vaccines (vacc_id, comirnaty, spikevax, janssen, vaxzevria)
            VALUES (?, ?, ?, ?, ?);
            """
        self.cur.execute(query, (vacc_id, vaccines['COMIRNATY'], vaccines['SPIKEVAX'],
                                 vaccines['JANSSEN'], vaccines['Vaxzevria']))
        self.conn.commit()

    def _insert_into_vacc_center_location(self, vacc_id: str, gps: tuple):
        """
        insert coordinates of center into vacc_center_location
        """
        query = """
            INSERT INTO vacc_center_location (vacc_id, latitude, longitude)
            VALUES (?, ?, ?);
            """
        self.cur.execute(query, (vacc_id, gps[0], gps[1]))
        self.conn.commit()

    def _insert_into_vacc_center_hours(self, vacc_id: str, open_hours: dict):
        """
        insert data about opening hours into table vacc_center_hours
        """
        query = """
            INSERT INTO vacc_center_hours (vacc_id, monday_open, monday_closed, tuesday_open, tuesday_closed, wednesday_open, 
                wednesday_closed, thursday_open, thursday_closed, friday_open, friday_closed, saturday_open, 
                saturday_closed, sunday_open, sunday_closed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """
        self.cur.execute(query, (vacc_id, open_hours['Pondělí'][0], open_hours['Pondělí'][1],
                                 open_hours['Úterý'][0], open_hours['Úterý'][1],
                                 open_hours['Středa'][0], open_hours['Středa'][1],
                                 open_hours['Čtvrtek'][0], open_hours['Čtvrtek'][1],
                                 open_hours['Pátek'][0], open_hours['Pátek'][1],
                                 open_hours['Sobota'][0], open_hours['Sobota'][1],
                                 open_hours['Neděle'][0], open_hours['Neděle'][1]))
        self.conn.commit()

    def _insert_into_vacc_center_info(self, vacc_id: str, info: dict):
        """
        insert information about center into table vacc_center_info
        """
        query = """
            INSERT INTO vacc_center_info (vacc_id, address, address_spec, phone, email, note,
                vaccines, add_info, capacity, changing_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """
        self.cur.execute(query, (vacc_id, info['Adresa'], info['Upřesnění polohy'], info['Telefon'], info['Email'],
                                 info['Poznámka'], str(info['Vakcíny'])[1: -1], str(info['Dodatečné informace'])[1: -1],
                                 info['Denní kapacita očkování'], str(info['Způsob změny termínu druhé dávky vakcíny'])[1: -1]))
        self.conn.commit()

    def _create_tables(self):
        """
        create all tables in db
        """
        queries = [""" CREATE TABLE IF NOT EXISTS vacc_center (
                    vacc_id TEXT PRIMARY KEY,
                    name TEXT,
                    region TEXT,
                    link TEXT
                    ); """,
                   """ CREATE TABLE IF NOT EXISTS vacc_center_type (
                    vacc_id TEXT PRIMARY KEY,
                    adult INTEGER,
                    teenage INTEGER,
                    child INTEGER,
                    without_registration INTEGER,
                    self_payers INTEGER
                    ); """,
                   """ CREATE TABLE IF NOT EXISTS vacc_center_vaccines (
                    vacc_id TEXT PRIMARY KEY,
                    comirnaty INTEGER,
                    spikevax INTEGER,
                    janssen INTEGER,
                    vaxzevria INTEGER
                    ); """,
                   """ CREATE TABLE IF NOT EXISTS vacc_center_location (
                    vacc_id TEXT PRIMARY KEY,
                    latitude REAL,
                    longitude REAL
                    ); """,
                   """ CREATE TABLE IF NOT EXISTS vacc_center_hours (
                    vacc_id TEXT PRIMARY KEY,
                    monday_open REAL,
                    monday_closed REAL,
                    tuesday_open REAL,
                    tuesday_closed REAL,
                    wednesday_open REAL,
                    wednesday_closed REAL,
                    thursday_open REAL,
                    thursday_closed REAL,
                    friday_open REAL,
                    friday_closed REAL,
                    saturday_open REAL,
                    saturday_closed REAL,
                    sunday_open REAL,
                    sunday_closed REAL
                    ); """,
                   """ CREATE TABLE IF NOT EXISTS vacc_center_info (
                    vacc_id TEXT PRIMARY KEY,
                    address TEXT,
                    address_spec TEXT,
                    phone TEXT,
                    email TEXT,
                    note TEXT,
                    vaccines TEXT,
                    add_info TEXT,
                    capacity TEXT,
                    changing_date TEXT
                    ); """,
                   """ CREATE TABLE IF NOT EXISTS locations (
                    name TEXT PRIMARY KEY,
                    latitude REAL,
                    longitude REAL
                    ); """]
        for query in queries:
            self.cur.execute(query)

    def _drop_tables(self):
        """
        drop all tables in db
        """
        tables = ['vacc_center', 'vacc_center_type', 'vacc_center_vaccines', 'vacc_center_location',
                  'vacc_center_hours', 'vacc_center_info', 'locations']
        for table in tables:
            query = f"DROP table IF EXISTS {table};"
            self.cur.execute(query)
        self.conn.commit()
