"""Stores alert events in SQLite."""
import sqlite3
import os
from datetime import datetime
import logging

class EventLogger:
    def __init__(self, db_path: str, db_dir: str):
        self.db_path = db_path
        
        # Ensure data directory exists
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            
        self._initialize_db()

    def _initialize_db(self):
        """Creates the logs table if it doesn't exist."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        ear_value REAL,
                        status TEXT NOT NULL
                    )
                """)
                conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Database initialization failed: {e}")

    def log_event(self, ear_value: float, status: str):
        """Logs a state change or significant event to the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute(
                    "INSERT INTO logs (timestamp, ear_value, status) VALUES (?, ?, ?)",
                    (timestamp, round(ear_value, 3), status)
                )
                conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Failed to log event: {e}")