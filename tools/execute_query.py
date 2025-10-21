from classes.PostgresConnection import PostgresConnection
from classes.Type import DBMS
import time


def get_db_connection(dbms: str, connection_string: str):
    match dbms:
        case DBMS.POSTGRESQL.name:
            return PostgresConnection(connection_string)
        case _:
            raise NotImplementedError(f"DBMS '{dbms}' não suportado ainda.")


def execute_query(data):
    start_time = time.time()
    try:
        connection_string = data.get("connection")
        query = data.get("query")
        dbms = data.get("dbms")
        if not connection_string or not query:
            return {
                "rows": [],
                "row_count": 0,
                "execution_time_ms": 0,
                "error": "Parâmetros obrigatórios ausentes (connection, query).",
            }
        db = get_db_connection(dbms, connection_string)
        if db is None:
            return {
                "rows": [],
                "row_count": 0,
                "execution_time_ms": 0,
                "error": f"DBMS '{dbms}' não suportado ainda.",
            }
        db.conectar()
        result_rows = db.executar_query(query)
        db.fechar()
        elapsed = (time.time() - start_time) * 1000
        return {
            "rows": result_rows,
            "row_count": len(result_rows),
            "execution_time_ms": round(elapsed, 2),
        }
    except Exception as e:
        elapsed = (time.time() - start_time) * 1000
        return {
            "rows": [],
            "row_count": 0,
            "execution_time_ms": round(elapsed, 2),
            "error": str(e),
        }
