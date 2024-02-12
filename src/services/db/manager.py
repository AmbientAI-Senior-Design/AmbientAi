import mysql.connector
from src.config import MYSQL_HOST, MYSQL_PASSWORD, MYSQL_PORT, MYSQL_USER


# Parent class for any database manager
class DatabaseManager:
    def __init__(self, db_name) -> None:
        try:
            self._conn = mysql.connector.connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=db_name,
                port=MYSQL_PORT
            )
            self.cursor = self._conn.cursor()
            print("Connected to MySQL database.")
        except mysql.connector.Error as err:
            print(f"{err}")

    def __enter__(self):
    # make a database connection and return it
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # make sure the dbconnection gets closed
        self._conn.close()

