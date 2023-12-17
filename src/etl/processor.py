import pandas as pd
import numpy as np

from tqdm import tqdm
from io import StringIO
from bs4 import BeautifulSoup
from db import DbInteractions, User, Gender, Role, Test, Question
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def _diagnosis_perceptual_modality(soup):
    values = [int(td.div.text) for td in soup.find_all("td", class_="nisVal")]
    names = [td.div.text for td in soup.find_all("td", class_="nisName")]
    return {name: value for name, value in zip(names, values)}


def _portrait_selection_method(soup):
    html_string = str(soup.find("div", id="szPlan1").table)
    df = pd.read_html(StringIO(html_string))[0].replace(np.nan, None)
    values = [[df[column].tolist()[3:15][:6], df[column].tolist()[3:15][6:]] for column in df]
    values = [[[i for i in l if i is not None] for l in row] for row in values]
    values = [[None if not i else int(i[0]) for i in row] for row in values]
    return {'Сетка результатов исследования': [i for row in values for i in row]}


def _five_factor_personality_questionnaire(soup):
    html_string = str(soup.find("div", class_="stdTbl").table)
    df = pd.read_html(StringIO(html_string))[0].replace(np.nan, None)
    d = dict()
    for _, row in df.iterrows():
        if type(row[0]) is str:
            for val in range(1, 16):
                if type(row[val]) is float:
                    d[f'{row[0]}-{row[16]}'] = int(row[val])
    return d


def _schema_questionnaire_jung(soup):
    values = [int(td.div.text.replace('%', '')) for td in soup.find_all("td", class_="nisVal")]
    names = [td.div.text for td in soup.find_all("td", class_="nisName")]
    return {name: value for name, value in zip(names, values)}


def _emotional_intelligence_test_hall(soup):
    values = [int(td.div.text) for td in soup.find_all("td", class_="nisVal")]
    names = [td.div.text for td in soup.find_all("td", class_="nisName")]
    return {name: value for name, value in zip(names, values)}


class Processor:
    TEST_URLS = {
        'Тест эмоционального интеллекта Холла': 'https://docs.google.com/spreadsheets/d/e/2PACX-1vR4jQUEh0HPzvbK0PZbywE7Cb3n3UUUTq0MfbVy_QgUiLgtqqEjhU6ME1uy3Dajl02sQCQzFFSwPYfU/pub?gid=0&single=true&output=csv',
        'Диагностика ведущей перцептивной модальности': 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSIgxdGm3ew_dUqtllDk_o7GdcdAati-LAOLOyskZWGqLejVFXaRb3eFU9DikVSVWns5hzkN15_TPbs/pub?gid=0&single=true&output=csv',
        'Пятифакторный опросник личности, 5PFQ': 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQ3eTmjwY8kYvuIllLtMoI7CXK7w1DhcXJB7ea2kI0Bq5i7HPkhzlvNcwtdx-97Dew4tgMXgHBuWUPO/pub?gid=0&single=true&output=csv',
        'Схемный опросник Янга, YSQ S3R': 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSbFAqpLF6H91fMnFapgqRaBfKZ-rYqS_UF0a-JdPenT-XtIBsVs2uvX699rZT9F6mOUxvZAL8Bx_WT/pub?gid=0&single=true&output=csv',
        'Метод портретных выборов': 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTMkSqvhyLzTajW5Ev5U84IcSZsimivd9F14RyDx3jNtW734yVLNTBLQqbM79dEKyeCNzAq-JlTQkl4/pub?gid=0&single=true&output=csv',
    }

    __parsers = {
        'Диагностика ведущей перцептивной модальности': _diagnosis_perceptual_modality,
        'Метод портретных выборов': _portrait_selection_method,
        'Пятифакторный опросник личности, 5PFQ': _five_factor_personality_questionnaire,
        'Схемный опросник Янга, YSQ S3R': _schema_questionnaire_jung,
        'Тест эмоционального интеллекта Холла': _emotional_intelligence_test_hall,
    }
    __user_id_shift = 10  # use for shift user_id for creating students

    def __init__(self, db_interactions: DbInteractions):
        self.db_interactions = db_interactions
        webdriver_service = Service(ChromeDriverManager().install())
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=webdriver_service, options=options)

    def process(self):
        self.db_interactions.create_necessary_instances()
        for test, crv_url in tqdm(self.TEST_URLS.items()):
            test_id = self.db_interactions.create_test(test)
            df = pd.read_csv(crv_url)
            for i, row in df.iterrows():
                if type(row['Ссылка на результат']) is str and 'https' in row['Ссылка на результат']:
                    url = row['Ссылка на результат']
                    self.driver.get(url)
                    soup = BeautifulSoup(self.driver.page_source, features="html.parser")
                    results = self.__parsers[test](soup)
                    student_id = int(row['№ п/п']) + self.__user_id_shift
                    self.__create_student(student_id)
                    for question_info, res in results.items():
                        question_id = self.db_interactions.create_question(test_id, f'Укажите значение "{question_info}"')
                        self.db_interactions.create_answer(question_id, student_id, res)
        self.driver.quit()

    def __create_student(self, id):
        if self.db_interactions.connection.session.query(User).filter(User.user_id == id).count() != 0:
            return
        profile = self.db_interactions.fake_ru.profile()
        if profile['sex'] == 'F':
            first_name = self.db_interactions.fake_ru.first_name_female()
            last_name = self.db_interactions.fake_ru.last_name_female()
            middle_name = self.db_interactions.fake_ru.middle_name_female()
            gender = Gender.FEMALE.value
        else:
            first_name = self.db_interactions.fake_ru.first_name_male()
            last_name = self.db_interactions.fake_ru.last_name_male()
            middle_name = self.db_interactions.fake_ru.middle_name_male()
            gender = Gender.MALE.value
        user_instance = User(
            user_id=id,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            birthday=profile['birthdate'],
            gender=gender,
            login=profile['username'] + ''.join(self.db_interactions.fake_ru.random_letters(length=3)).lower(),
            password=self.db_interactions.fake_ru.password(),
            phone_number=self.db_interactions.fake_ru.phone_number(),
            role=Role.STUDENT.value,
            group_id=1,
            study_direction_id=1
        )
        self.db_interactions.connection.session.add(user_instance)
        self.db_interactions.connection.session.commit()


if __name__ == '__main__':
    db_interactions = DbInteractions(
        host='localhost',
        port='5434',
        user='postgres',
        password='postgres',
        db_name='student_testyfier',
        rebuild_db=True
    )
    db_interactions.recreate_tables()
    processor = Processor(db_interactions)
    processor.process()
