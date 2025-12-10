from classes.Connection.PostgresConnection import PostgresConnection
from classes.MCPUtils.Type import DBMS
from classes.Admin.TokenCredential import TokenCredential
import time


def get_db_connection(dbms: str, connection_string: str):
    match dbms:
        case DBMS.POSTGRESQL.name:
            return PostgresConnection(connection_string)
        case _:
            raise NotImplementedError(f"DBMS '{dbms}' não suportado ainda.")


def tool_execute_query(credential_token: str, sql_query: str):
    start_time = time.time()
    try:
        if not credential_token or not sql_query:
            return {
                "rows": [],
                "row_count": 0,
                "execution_time_ms": 0,
                "error": "Parâmetros obrigatórios ausentes (credential_token, sql_query).",
            }

        # Buscar credenciais usando o token
        store = TokenCredential()
        token_data = store.get_credential(credential_token)
        if not token_data:
            return {
                "rows": [],
                "row_count": 0,
                "execution_time_ms": 0,
                "error": "Token não encontrado ou expirado.",
            }

        token_db_type = token_data.get("db_type")
        credential = token_data.get("credential") or {}

        # Mapear o db_type retornado (ex: "postgresql") para o nome do Enum (ex: "POSTGRESQL")
        try:
            dbms = DBMS(token_db_type).name
        except Exception:
            return {
                "rows": [],
                "row_count": 0,
                "execution_time_ms": 0,
                "error": f"Tipo de banco de dados '{token_db_type}' não suportado.",
            }

        # Construir connection string a partir das credenciais
        connection_string = None
        if dbms == DBMS.POSTGRESQL.name:
            user = credential.get("user")
            password = credential.get("password")
            host = credential.get("host")
            port = credential.get("port")
            database = (
                credential.get("database") or credential.get("dbname") or "postgres"
            )
            connection_string = (
                f"postgresql://{user}:{password}@{host}:{port}/{database}"
            )
        else:
            return {
                "rows": [],
                "row_count": 0,
                "execution_time_ms": 0,
                "error": f"DBMS '{dbms}' não suportado ainda.",
            }

        db = get_db_connection(dbms, connection_string)

        db.connect()
        result_rows = db.execute_query(sql_query)
        db.close()
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
