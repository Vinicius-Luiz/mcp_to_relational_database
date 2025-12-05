import sqlite3
import uuid
import json
from datetime import datetime


class TokenCredential:
    SQL_CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS token_credentials (
        token TEXT PRIMARY KEY,
        credential TEXT NOT NULL,
        db_type TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """

    SQL_CREATE_TOKEN = """
    INSERT INTO token_credentials (token, credential, db_type, created_at)
    VALUES (?, ?, ?, ?)
    """

    SQL_GET_CREDENTIAL = """
    SELECT credential, db_type, created_at
    FROM token_credentials
    WHERE token = ?
    """

    SQL_DELETE_CREDENTIAL = """
    DELETE FROM token_credentials
    WHERE token = ?
    """

    def __init__(self, db_path="credentials.db"):
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(self.SQL_CREATE_TABLE)

        conn.commit()
        conn.close()

    def create_token(self, credential: dict, db_type: str) -> str:
        token = str(uuid.uuid4())
        created_at = datetime.now().isoformat()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            self.SQL_CREATE_TOKEN,
            (token, json.dumps(credential), db_type, created_at),
        )

        conn.commit()
        conn.close()

        return token

    def get_credential(self, token: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            self.SQL_GET_CREDENTIAL,
            (token,),
        )

        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        credential_json, db_type, created_at = row

        return {
            "token": token,
            "credential": json.loads(credential_json),
            "db_type": db_type,
            "created_at": created_at,
        }

    def delete_credential(self, token: str) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(self.SQL_DELETE_CREDENTIAL, (token,))

        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()

        return deleted


if __name__ == "__main__":
    store = TokenCredential()

    # Criar token e credencial
    token = store.create_token(
        credential={"user": "db_user", "password": "12345", "host": "localhost"},
        db_type="postgresql",
    )
    print("Token criado:", token)

    # Buscar credencial
    data = store.get_credential(token)
    print("Credencial encontrada:", data)

    # Remover credencial
    removed = store.delete_credential(token)
    print("Credencial removida:", removed)
