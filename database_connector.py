import sqlite3
from sqlite3 import Error
from config import DB_FILE


class DatabaseConnector():
    db_file = DB_FILE

    def __init__(self):
        self.conn = None
        try:
            self.conn = sqlite3.connect(self.db_file)
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
    db = DatabaseConnector()
    db.create_example_table()
    db.insert_data_into_example_table(1, 'Pepa', 'Pfizer')
    db.insert_data_into_example_table(2, 'Franta', 'Moderna')

    db.read_table("SELECT * from example")
