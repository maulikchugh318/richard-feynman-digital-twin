import sqlite3
from datetime import datetime

from config import settings


class LongTermMemory:

    def __init__(self):

        self.conn = sqlite3.connect(
            settings.MEMORY_DB_PATH,
            check_same_thread=False
        )

        self.create_table()

    def create_table(self):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS memories(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT,
                created_at TEXT
            )
            """
        )

        self.conn.commit()

    def store_memory(
        self,
        content
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT INTO memories(content, created_at)
            VALUES(?, ?)
            """,
            (
                content,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )

        self.conn.commit()

    def get_memories(self):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT content
            FROM memories
            ORDER BY id DESC
            """
        )

        return [
            row[0]
            for row in cursor.fetchall()
        ]

    def get_memories_with_time(self):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT id, content, created_at
            FROM memories
            ORDER BY id DESC
            """
        )

        return cursor.fetchall()

    def count_memories(self):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM memories
            """
        )

        return cursor.fetchone()[0]


    def clear_memories(self):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            DELETE FROM memories
            """
        )

        self.conn.commit()    