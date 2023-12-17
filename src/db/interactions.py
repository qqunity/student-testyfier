from db import (PostgreSQLConnection, Base, Gender, Role, User, Group, Degree, StudyDirection, Subject,
                TeacherSubject, StudyDirectionSubject, TestType, Test, TestSubject, TestFeedback, Action,
                UserTestAction, QuestionType, Question, UserQuestionAction, Answer)
from faker import Factory
from utils import DefaultProvider
from sqlalchemy import text


class DbInteractions:

    def __init__(self, host, port, user, password, db_name, rebuild_db=False):
        self.connection = PostgreSQLConnection(
            host=host,
            port=port,
            user=user,
            password=password,
            db_name=db_name,
            rebuild_db=rebuild_db
        )

        self.engine = self.connection.connection.engine
        self.fake_ru = Factory.create('ru_RU')
        self.fake_ru.add_provider(DefaultProvider)
        self.fake_en = Factory.create('en_PH')
        self.fake_en.add_provider(DefaultProvider)

    def recreate_tables(self):
        for table in Base.metadata.tables.keys():
            self.connection.execute_query(text('DROP TABLE IF EXISTS "{table}" CASCADE'))
            Base.metadata.tables[f'{table}'].create(self.engine)
