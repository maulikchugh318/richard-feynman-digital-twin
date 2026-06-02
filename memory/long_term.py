import sqlite3

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
                content TEXT
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
            INSERT INTO memories(content)
            VALUES(?)
            """,
            (content,)
        )

        self.conn.commit()

    def get_memories(self):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT content
            FROM memories
            """
        )

        return [
            row[0]
            for row in cursor.fetchall()
        ]