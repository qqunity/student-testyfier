from enum import Enum

from sqlalchemy import Column, ForeignKey, VARCHAR, BIGINT, SMALLINT, BOOLEAN, Date, DateTime, Text, Interval
from sqlalchemy.dialects.postgresql import JSONB, ENUM as PgEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Gender(Enum):
    MALE = 0
    FEMALE = 1


class Role(Enum):
    ADMIN = 0
    STUDENT = 1
    TEACHER = 2
    EXPERT = 3


class Group(Base):
    __tablename__ = 'group'

    group_id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    name = Column(VARCHAR(10), nullable=False)
    archived = Column(BOOLEAN, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<Group #{self.group_id} name="{self.name}">'


class StudyDirection(Base):
    __tablename__ = 'study_direction'

    study_direction_id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    name = Column(VARCHAR(64), nullable=False)
    degree = Column(SMALLINT, nullable=False)
    archived = Column(BOOLEAN, nullable=False, default=False)
    speciality_code = Column(VARCHAR(10), nullable=False)

    def __repr__(self):
        return f'<StudyDirection #{self.study_direction_id} name="{self.name}">'


class User(Base):
    __tablename__ = 'user'

    user_id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    first_name = Column(VARCHAR(64), nullable=False)
    last_name = Column(VARCHAR(64), nullable=False)
    middle_name = Column(VARCHAR(64), nullable=True)
    birthday = Column(Date, nullable=True)
    gender = Column(SMALLINT, nullable=False)
    login = Column(VARCHAR(64), nullable=False, unique=True)
    password = Column(VARCHAR(64), nullable=False)
    phone_number = Column(VARCHAR(64), nullable=True)
    photo_url = Column(VARCHAR(120), nullable=True)
    role = Column(SMALLINT, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_logged_at = Column(DateTime(timezone=True), nullable=True)
    deleted = Column(BOOLEAN, nullable=False, default=False)
    group_id = Column(BIGINT, ForeignKey('group.group_id', ondelete='SET NULL'), nullable=True, index=True)
    study_direction_id = Column(BIGINT, ForeignKey('study_direction.study_direction_id', ondelete='SET NULL'),
                                nullable=True, index=True)

    group = relationship('Group', backref='users')
    study_direction = relationship('StudyDirection', backref='users')

    def __repr__(self):
        return f'<User #{self.user_id} first_name="{self.first_name}" last_name="{self.last_name}" login="{self.login}">'


class Degree(Enum):
    BACHELOR = 0
    MASTER = 1
    SPECIALIST = 2
    POSTGRADUATE = 3


class Subject(Base):
    __tablename__ = 'subject'

    subject_id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    name = Column(VARCHAR(100), nullable=False)
    archived = Column(BOOLEAN, nullable=False, default=False)

    def __repr__(self):
        return f'<Subject #{self.subject_id} name="{self.name}">'


class TeacherSubject(Base):
    __tablename__ = 'teacher_subject'

    teacher_subject_id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    teacher_id = Column(BIGINT, ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    subject_id = Column(BIGINT, ForeignKey('subject.subject_id', ondelete='CASCADE'), nullable=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)

    teacher = relationship('User', backref='teacher_subjects')
    subject = relationship('Subject', backref='teacher_subjects')

    def __repr__(self):
        return f'<TeacherSubject #{self.teacher_subject_id} teacher_id={self.teacher_id} subject_id={self.subject_id}>'


class StudyDirectionSubject(Base):
    __tablename__ = 'study_direction_subject'

    study_direction_subject_id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    study_direction_id = Column(BIGINT, ForeignKey('study_direction.study_direction_id', ondelete='CASCADE'),
                                nullable=False)
    subject_id = Column(BIGINT, ForeignKey('subject.subject_id', ondelete='CASCADE'), nullable=False)

    study_direction = relationship('StudyDirection', backref='study_direction_subjects')
    subject = relationship('Subject', backref='study_direction_subjects')

    def __repr__(self):
        return f'<StudyDirectionSubject #{self.study_direction_subject_id} study_direction_id={self.study_direction_id} subject_id={self.subject_id}>'


class TestType(Enum):
    PSYCHOLOGICAL = 0
    EXAM = 1
    TEST = 2


class Test(Base):
    __tablename__ = 'test'

    test_id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    reviewer_id = Column(BIGINT, ForeignKey('user.user_id', ondelete='SET NULL'), nullable=True)
    name = Column(VARCHAR(100), nullable=False)
    type = Column(PgEnum(TestType, name='test_type'), nullable=False)
    description = Column(Text, nullable=True)
    duration = Column(Interval, nullable=False)
    archived = Column(BOOLEAN, nullable=False, default=False)

    reviewer = relationship('User', backref='tests')

    def __repr__(self):
        return f'<Test #{self.test_id} name="{self.name}">'


class TestSubject(Base):
    __tablename__ = 'test_subject'

    test_subject_id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    test_id = Column(BIGINT, ForeignKey('test.test_id', ondelete='CASCADE'), nullable=False)
    subject_id = Column(BIGINT, ForeignKey('subject.subject_id', ondelete='CASCADE'), nullable=False)

    test = relationship('Test', backref='test_subjects')
    subject = relationship('Subject', backref='test_subjects')

    def __repr__(self):
        return f'<TestSubject #{self.test_subject_id} test_id={self.test_id} subject_id={self.subject_id}>'


class TestFeedback(Base):
    __tablename__ = 'test_feedback'

    test_feedback_id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    test_id = Column(BIGINT, ForeignKey('test.test_id', ondelete='CASCADE'), nullable=False)
    user_id = Column(BIGINT, ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    comment = Column(Text, nullable=False)
    score = Column(SMALLINT, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    test = relationship('Test', backref='test_feedbacks')
    user = relationship('User', backref='test_feedbacks')

    def __repr__(self):
        return f'<TestFeedback #{self.test_feedback_id} test_id={self.test_id} user_id={self.user_id}>'


class Action(Enum):
    CREATE = 0
    UPDATE = 1
    DELETE = 2


class UserTestAction(Base):
    __tablename__ = 'user_test_action'

    user_test_action_id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    test_id = Column(BIGINT, ForeignKey('test.test_id', ondelete='CASCADE'), nullable=False)
    user_id = Column(BIGINT, ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    action = Column(SMALLINT, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    test = relationship('Test', backref='user_test_actions')
    user = relationship('User', backref='user_test_actions')

    def __repr__(self):
        return f'<UserTestAction #{self.user_test_action_id} test_id={self.test_id} user_id={self.user_id} action={self.action}>'


class QuestionType(Enum):
    SINGLE_ANSWER = 0
    MULTIPLE_ANSWERS = 1
    TEXT_ANSWER = 2


class Question(Base):
    __tablename__ = 'question'

    question_id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    test_id = Column(BIGINT, ForeignKey('test.test_id', ondelete='CASCADE'), nullable=False)
    description = Column(Text, nullable=False)
    type = Column(PgEnum(QuestionType, name='question_type'), nullable=False)
    answer_options = Column(JSONB, nullable=True)
    required = Column(BOOLEAN, nullable=False, default=True)
    deleted = Column(BOOLEAN, nullable=False, default=False)

    test = relationship('Test', backref='questions')

    def __repr__(self):
        return f'<Question #{self.question_id} test_id={self.test_id}>'


class UserQuestionAction(Base):
    __tablename__ = 'user_question_action'

    user_question_action_id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    question_id = Column(BIGINT, ForeignKey('question.question_id', ondelete='CASCADE'), nullable=False)
    user_id = Column(BIGINT, ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    action = Column(SMALLINT, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    question = relationship('Question', backref='user_question_actions')
    user = relationship('User', backref='user_question_actions')

    def __repr__(self):
        return f'<UserQuestionAction #{self.user_question_action_id} question_id={self.question_id} user_id={self.user_id} action={self.action}>'


class Answer(Base):
    __tablename__ = 'answer'

    answer_id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    question_id = Column(BIGINT, ForeignKey('question.question_id', ondelete='CASCADE'), nullable=False)
    user_id = Column(BIGINT, ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    answer = Column(JSONB, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    question = relationship('Question', backref='answers')
    user = relationship('User', backref='answers')

    def __repr__(self):
        return f'<Answer #{self.answer_id} question_id={self.question_id} user_id={self.user_id}>'
