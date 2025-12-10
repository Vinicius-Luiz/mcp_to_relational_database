import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import os

load_dotenv()


class LogManager:
    SQL_CREATE_LOGS_TABLE = """
        CREATE TABLE IF NOT EXISTS logs_mcp (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            usuario TEXT,
            tool TEXT NOT NULL,
            status TEXT NOT NULL,
            execution_time REAL NOT NULL
        );
    """
    # NOTA: as tabelas `users` e `connections` foram removidas intencionalmente.

    SQL_INSERT_LOG = """
        INSERT INTO logs_mcp (timestamp, usuario, tool, status, execution_time)
        VALUES (?, ?, ?, ?, ?);
    """

    SQL_SELECT_LOGS = """
        SELECT timestamp, usuario, tool, status, execution_time
        FROM logs_mcp
        ORDER BY id DESC;
    """

    # ================================
    # CONSTRUTOR
    # ================================
    def __init__(self):
        """
        Inicializa o LogManager.
        """
        self.db_path = os.getenv("LOGGER_DB_PATH")
        if not self.db_path:
            raise ValueError(
                "DB_PATH não definido — passe db_path ou defina a variável de ambiente DB_PATH."
            )
        self._init_db()

    # ================================
    # Inicializa banco e tabelas
    # ================================
    def _init_db(self) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(self.SQL_CREATE_LOGS_TABLE)

        conn.commit()
        conn.close()

    # ================================
    # Insere log
    # ================================
    def insert_log(self, log_entry: Dict[str, Any]) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            self.SQL_INSERT_LOG,
            (
                log_entry.get(
                    "timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ),
                log_entry.get("usuario", "anonymous"),
                log_entry.get("tool", "unknown"),
                log_entry.get("status", "unknown"),
                log_entry.get("execution_time", 0.0),
            ),
        )

        conn.commit()
        conn.close()

    # ================================
    # Lista todos os logs
    # ================================
    def get_logs(self) -> List[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(self.SQL_SELECT_LOGS)
        rows = cursor.fetchall()
        conn.close()

        return [
            {
                "timestamp": row[0],
                "usuario": row[1],
                "tool": row[2],
                "status": row[3],
                "execution_time": row[4],
            }
            for row in rows
        ]

    # ================================
    # Helper para registrar execução de tool
    # ================================
    def log_tool_execution(
        self,
        tool_name: str,
        status: str,
        execution_time: float,
        usuario: str = "anonymous",
    ) -> None:
        """
        Função auxiliar para registrar a execução de uma ferramenta MCP.

        Args:
            tool_name: Nome da ferramenta executada
            status: Status da execução (success, error, etc.)
            execution_time: Tempo de execução em segundos
            usuario: Usuário que executou a ferramenta (padrão: "anonymous")
        """
        self.insert_log(
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "usuario": usuario,
                "tool": tool_name,
                "status": status,
                "execution_time": execution_time,
            }
        )


# ================================
# Exemplo de uso (se executado diretamente)
# ================================
if __name__ == "__main__":
    # Se preferir, defina DB_PATH no seu .env ou passe um caminho diretamente ao criar LogManager
    lm = LogManager()  # ou LogManager(db_path="meu_banco.db")

    lm.log_tool_execution("importer", "success", 1.23, usuario="vinicius")

    logs = lm.get_logs()
    for l in logs[:5]:
        print(l)
