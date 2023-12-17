import sqlalchemy

from sqlalchemy.orm import sessionmaker
from sqlalchemy import text


class PostgreSQLConnection:

    def __init__(self, host, port, user, password, db_name, rebuild_db=False):
        self.user = user
        self.password = password
        self.db_name = db_name

        self.host = host
        self.port = port

        self.rebuild_db = rebuild_db
        self.connection = self._connect()

        session = sessionmaker(self.connection.engine)
        self.session = session()

    def _get_connection(self, db_created=False):
        engine = sqlalchemy.create_engine(
            f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name if db_created else ""}',
            client_encoding='utf8'
        )
        return engine.connect()

    def _connect(self):
        connection = self._get_connection()
        if self.rebuild_db:
            connection.execute(text(f'DROP DATABASE IF EXISTS {self.db_name}'))
            connection.execute(text(f'CREATE DATABASE {self.db_name}'))
            connection.close()
        return self._get_connection(db_created=True)

    def execute_query(self, query):
        res = self.connection.execute(query)
        return res