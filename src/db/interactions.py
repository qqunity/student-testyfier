import datetime

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
        for table in reversed(Base.metadata.tables.keys()):
            Base.metadata.tables[f'{table}'].drop(self.engine, checkfirst=True)
        for table in Base.metadata.tables.keys():
            Base.metadata.tables[f'{table}'].create(self.engine)

    def __create_group(self):
        group_instance = Group(
            name='М23-504'
        )
        self.connection.session.add(group_instance)
        self.connection.session.commit()

    def __create_study_direction(self):
        study_direction_instance = StudyDirection(
            name='Программная инженерия',
            degree=Degree.MASTER.value,
            speciality_code='09.04.04'
        )
        self.connection.session.add(study_direction_instance)
        self.connection.session.commit()

    def __create_subject(self):
        subject_instance = Subject(
            name='Проектирование информационных систем'
        )
        self.connection.session.add(subject_instance)
        self.connection.session.commit()

    def __create_teacher(self):
        user_instance = User(
            first_name='Дарья',
            last_name='Тихомирова',
            middle_name='Валерьевна',
            gender=Gender.FEMALE.value,
            login='dvtihomirova',
            password='12345678',
            role=Role.TEACHER.value,
        )
        self.connection.session.add(user_instance)
        self.connection.session.commit()

    def __create_teacher_subject(self):
        teacher_subject_instance = TeacherSubject(
            teacher_id=1,
            subject_id=1
        )
        self.connection.session.add(teacher_subject_instance)
        self.connection.session.commit()

    def __create_study_direction_subject(self):
        study_direction_subject_instance = StudyDirectionSubject(
            study_direction_id=1,
            subject_id=1
        )
        self.connection.session.add(study_direction_subject_instance)
        self.connection.session.commit()

    def create_necessary_instances(self):
        self.__create_group()
        self.__create_study_direction()
        self.__create_subject()
        self.__create_teacher()
        self.__create_teacher_subject()
        self.__create_study_direction_subject()

    def create_test(self, name) -> int:
        test_instance = Test(
            name=name,
            reviewer_id=1,
            type=TestType.PSYCHOLOGICAL,
            duration=datetime.timedelta(hours=1, minutes=30)
        )
        self.connection.session.add(test_instance)
        self.connection.session.commit()
        test_id = self.connection.session.query(Test).filter(Test.name == name).first().test_id
        test_subject_instance = TestSubject(
            test_id=test_id,
            subject_id=1
        )
        self.connection.session.add(test_subject_instance)
        user_test_action_instance = UserTestAction(
            user_id=1,
            test_id=test_id,
            action=Action.CREATE.value
        )
        self.connection.session.add(user_test_action_instance)
        self.connection.session.commit()
        return test_id

    def create_question(self, test_id, description) -> int:
        question_instance = Question(
            test_id=test_id,
            type=QuestionType.TEXT_ANSWER,
            description=description
        )
        self.connection.session.add(question_instance)
        self.connection.session.commit()
        question_id = self.connection.session.query(Question).filter(Question.test_id == test_id).filter(
            Question.description == description).first().question_id
        user_question_action_instance = UserQuestionAction(
            user_id=1,
            question_id=question_id,
            action=Action.CREATE.value
        )
        self.connection.session.add(user_question_action_instance)
        self.connection.session.commit()
        return question_id

    def create_answer(self, question_id, user_id, answer) -> int:
        answer_instance = Answer(
            question_id=question_id,
            user_id=user_id,
            answer=answer
        )
        self.connection.session.add(answer_instance)
        self.connection.session.commit()
        answer_id = self.connection.session.query(Answer).filter(Answer.question_id == question_id).filter(
            Answer.user_id == user_id).first().answer_id
        return answer_id
