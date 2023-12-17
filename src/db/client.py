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
        self.connection = self._get_connection()

        session = sessionmaker(self.connection.engine)
        self.session = session()

    def _get_connection(self):
        engine = sqlalchemy.create_engine(
            f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}',
            client_encoding='utf8'
        )
        return engine.connect()

    def execute_query(self, query):
        res = self.connection.execute(query)
        return res