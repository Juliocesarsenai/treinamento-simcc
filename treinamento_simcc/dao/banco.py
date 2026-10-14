import os
import psycopg2
from psycopg2.extras import RealDictCursor


class Connection:
    def __init__(
        self,
        database: str = os.getenv("DATABASE", "postgres"),
        user: str = os.getenv("PG_USER", "postgres"),
        password: str = os.getenv("PASSWORD", "qualquer_uma"),
        host: str = os.getenv("HOST", "127.0.0.1"),
        port: int = int(os.getenv("PORT", "5437")),
    ):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        # Correção do psycopg2 e adição do RealDictCursor para retornar JSON
        self.connection = psycopg2.connect(
            database=self.database,
            user=self.user,
            host=self.host,
            password=self.password,
            port=self.port,
            cursor_factory=RealDictCursor
        )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            try:
                self.connection.close()
            except Exception as e:
                print(f"Erro ao fechar a conexão: {e}")
                raise

    def select(self, script_sql: str, parameters: list = []):
        with self.connection.cursor() as cursor:
            cursor.execute(script_sql, parameters)
            return cursor.fetchall()

    def exec(self, script_sql: str, parameters: list = []):
        with self.connection.cursor() as cursor:
            cursor.execute(script_sql, parameters)
            self.connection.commit()

    def execmany(self, script_sql: str, parameters: list = []):
        with self.connection.cursor() as cursor:
            cursor.executemany(script_sql, parameters)
            self.connection.commit()