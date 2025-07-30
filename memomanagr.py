import sqlite3
import pandas as pd
from datetime import datetime

class MemoryManager:
    def __init__(self, db_path="memory.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        c = self.conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                llm_name TEXT,
                prompt TEXT,
                response TEXT,
                timestamp TEXT
            )
        """)
        self.conn.commit()

    def save_interaction(self, llm_name, prompt, response):
        c = self.conn.cursor()
        c.execute(
            "INSERT INTO conversations (llm_name, prompt, response, timestamp) VALUES (?, ?, ?, ?)",
            (llm_name, prompt, response, datetime.utcnow().isoformat())
        )
        self.conn.commit()

    def load_all(self):
        return pd.read_sql_query("SELECT * FROM conversations", self.conn)

    def analyze_by_llm(self):
        df = self.load_all()
        if df.empty:
            return None
        grouped = df.groupby("llm_name").size()
        return grouped.to_dict()

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    mm = MemoryManager()
    mm.save_interaction("MainLLM", "Hello", "Hi there!")
    print(mm.load_all())
    print(mm.analyze_by_llm())
    mm.close()
