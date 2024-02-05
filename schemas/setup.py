"""
This script is used to create databases and schemas from the files in the current directory.
To create a database, create a new folder. To define a schema, create a new file in the folder.
To run, use the command `python setup.py` in the terminal.
"""

import os
import sys
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

    #def __enter__(self):
     #   pass

    #def __exit__(self, exc_type, exc_value, traceback):
        
     #   self._connector.commit()
      #  self._cursor.close()
       # self._connector.close()
    

    def create_database(self, database_name: str) -> None:
        self._cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        self._connector.commit()

    def create_table_from_file(self, database_name: str, file_path: str) -> None:
        with open(file_path, 'r', encoding='utf-8') as file:
            query = file.read()
        self._cursor.execute(f"USE {database_name}")
        for statements in self._cursor.execute(query, multi=True):
            pass
        self._connector.commit()

    def insert_data(self, database_name: str, table_name: str, image_name: str, image_path: str  ) -> None:
        self._cursor.execute(f"USE {database_name}")
        with open(image_path, 'rb') as file:
            image_data = file.read()
            insert_query = f"INSERT INTO {table_name} (image_name, image_path) VALUES (%s, %s)"
            self._cursor.execute(insert_query, (image_name, image_path))
            self._connector.commit()

    def create_db():
        with DatabaseManager() as db:

            for root, dirs, files in os.walk('.'):
                for dir in dirs:
                    db.create_database(dir)
                    for file in os.listdir(dir):
                        if file.endswith('.sql'):
                            file_path = os.path.join(root, dir, file)
                            db.create_table_from_file(dir, file_path)
