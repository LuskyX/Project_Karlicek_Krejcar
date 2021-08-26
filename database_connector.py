import sqlite3
from sqlite3 import Error

DB_FILE = "db/database.db"

class DatabaseConnector():
    def __init__(self, DB_FILE):
        self.conn = None
        try:
            self.conn = sqlite3.connect(DB_FILE)
        except Error as e:
            print(e)
        self.cur = self.conn.cursor()

    def create_example_table(self):
        query = """ CREATE TABLE IF NOT EXISTS example (
                    id integer PRIMARY KEY,
                    name text NOT NULL,
                    vaccine text
                    ); """
        self.cur.execute(query)

    def insert_data_into_example_table(self, id, name, vaccine):
        query = """
            INSERT INTO example (id, name, vaccine)
            VALUES (?, ?, ?)
            """
        self.cur.execute(query, (id, name, vaccine))
        self.conn.commit()

    def read_table(self, query):
        data = []
        self.cur.execute(query)
        data = self.cur.fetchall()
        return data

if __name__ == '__main__':
    db = DatabaseConnector(DB_FILE)
    db.create_example_table()
    db.insert_data_into_example_table(1, 'Pepa', 'Pfizer')
    db.insert_data_into_example_table(2, 'Franta', 'Moderna')

    db.read_table("SELECT * from example")
