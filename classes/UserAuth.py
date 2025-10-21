import sqlite3
import hashlib
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()

DB_PATH = os.getenv("DB_PATH")


class UserAuth:
    @staticmethod
    def hash_key(key: str) -> str:
        return hashlib.sha256(key.encode("utf-8")).hexdigest()

    @staticmethod
    def login(api_mcp_key: str) -> Optional[int]:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        hashed = UserAuth.hash_key(api_mcp_key)
        cursor.execute("SELECT id FROM users WHERE api_mcp_key = ?", (hashed,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return row[0]
        return None

    @staticmethod
    def add_user(api_mcp_key: str) -> int:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        hashed = UserAuth.hash_key(api_mcp_key)
        cursor.execute(
            "INSERT INTO users (api_mcp_key, created_at) VALUES (?, ?)",
            (hashed, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id

    @staticmethod
    def add_connection(user_id: int, dbms: str, connection_string: str) -> int:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO connections (user_id, dbms, connection_string, created_at) VALUES (?, ?, ?, ?)",
            (
                user_id,
                dbms,
                connection_string,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )
        conn.commit()
        conn.close()
        return 1

    @staticmethod
    def remove_connection(user_id: int, dbms: str) -> int:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM connections WHERE user_id = ? AND dbms = ?", (user_id, dbms)
        )
        conn.commit()
        conn.close()
        return 1

    @staticmethod
    def get_connection(user_id: int, dbms: str) -> Optional[str]:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT connection_string FROM connections WHERE user_id = ? AND dbms = ?",
            (user_id, dbms),
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            return row[0]
        return None
