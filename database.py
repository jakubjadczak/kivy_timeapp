from dotenv import load_dotenv
from os import getenv
import sqlite3
from sys import argv
load_dotenv()


class DataBase:
    def __init__(self):
        self.connection = sqlite3.connect(getenv('DB_NAME'))
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def _create_table(self):
        self.cursor.execute('CREATE TABLE time_app'
                            '(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, hrs TEXT, min TEXT,'
                            'sec TEXT, mcrsec TEXT)')
        self.connection.commit()

    def insert(self, name: str, hrs: str, min: str, sec: str, mcrsec: str):
        self.cursor.execute('INSERT INTO time_app VALUES (?, ?, ?, ?, ?, ?)',
                            (None, name, hrs, min, sec, mcrsec))
        self.connection.commit()

    def reading_all(self):
        self.cursor.execute('SELECT * FROM time_app')
        rows = self.cursor.fetchall()
        return rows

    def reading_one(self, idt):
        """

        :param idt: id
        :return: row as string
        """
        self.cursor.execute(f'SELECT * FROM time_app WHERE id={idt}')
        row = self.cursor.fetchone()
        row = [str(r) for r in row]
        row_time = row[-4:]
        row_name = row[0:2]
        row.clear()
        time = ' : '.join(row_time)
        name = '       '.join(row_name)
        return name + '  ' + time

    def delete_by_id(self, idt):
        self.cursor.execute(f'DELETE FROM time_app WHERE id={idt}')
        self.connection.commit()

    def edit_by_id(self, idt: int, new_name: str):
        self.cursor.execute(f'UPDATE time_app SET name=? WHERE id=?', (new_name, idt))
        self.connection.commit()


if len(argv) > 1 and argv[1] == 'setup':
    """
    Initializing Database
    Usage: python database.py setup
    """
    print('Table creating...')
    db = DataBase()
    db._create_table()

if len(argv) > 1 and argv[1] == 'show':
    db = DataBase()
    print(db.reading_all())
