import sqlite3

class Database_Manager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            print(f"Failed to connect to {self.db_path}: {e}")
            raise

    def execute_query(self, query, params=None):
        if not self.cursor:
            raise ValueError("Database connection is not established.")
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
        except sqlite3.Error as e:
            return e

    def fetchall(self):
        if not self.cursor:
            raise ValueError("Cursor is not initialized.")
        return self.cursor.fetchall()

    def commit(self):
        if self.connection:
            self.connection.commit()

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None

    # Add these methods to support the 'with' statement
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()