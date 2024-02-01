"""
This script is used to create databases and schemas from the files in the current directory.
To create a database, create a new folder. To define a schema, create a new file in the folder.
To run, use the command `python setup.py` in the terminal.
"""

import os
import mysql.connector
from src.config import MYSQL_PORT, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_USER


class DatabaseManager:

    def __init__(self) -> None:
        self._connector = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            port=MYSQL_PORT
        )
        self._cursor = self._connector.cursor()

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        self._cursor.close()
        self._connector.close()
        self._connector.commit()

    def create_database(self, database_name: str) -> None:
        self._cursor.execute(f"CREATE DATABASE {database_name}")

    def create_table_from_file(self, database_name: str, file_path: str) -> None:
        with open(file_path, 'r', encoding='utf-8') as file:
            query = file.read()
            self._cursor.execute(f"USE {database_name}")
            self._cursor.execute(query)


with DatabaseManager() as db:

    for root, dirs, files in os.walk('.'):
        for dir in dirs:
            db.create_database(dir)
            for file in os.listdir(dir):
                if file.endswith('.sql'):
                    file_path = os.path.join(root, dir, file)
                    db.create_table_from_file(dir, file_path)
