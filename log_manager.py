import sqlite3
from datetime import datetime
from typing import List, Dict, Any
from dotenv import load_dotenv
import os

load_dotenv()

DB_PATH = os.getenv("DB_PATH")


# ====== Inicializa banco e tabela ======
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS execution_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            tool TEXT NOT NULL,
            status TEXT NOT NULL,
            execution_time REAL NOT NULL
        );
    """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            api_mcp_key TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL
        );
    """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS connections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            dbms TEXT NOT NULL,
            connection_string TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    """
    )
    conn.commit()
    conn.close()


# ====== Insere log ======
def insert_log(log_entry: Dict[str, Any]):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO execution_logs (timestamp, tool, status, execution_time)
        VALUES (?, ?, ?, ?);
    """,
        (
            log_entry.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            log_entry.get("tool", "unknown"),
            log_entry.get("status", "unknown"),
            log_entry.get("execution_time", 0.0),
        ),
    )
    conn.commit()
    conn.close()


# ====== Lista todos os logs ======
def get_logs() -> List[Dict[str, Any]]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT timestamp, tool, status, execution_time FROM execution_logs ORDER BY id DESC;"
    )
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "timestamp": row[0],
            "tool": row[1],
            "status": row[2],
            "execution_time": row[3],
        }
        for row in rows
    ]
