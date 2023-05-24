import itertools
import json
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from rest_framework.test import APITestCase


class ApiTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user_data = {'user_name': 'test', 'user_type': 'test', 'login': 'test', 'password': 'test',
                         'create_test_permission': False}

    def UserTestPost(self):
        user_response = requests.post("http://localhost:8000/user", self.user_data)
        self.assertEqual(user_response.status_code, 200)

        user_json_response = json.loads(user_response.text)
        self.user_id = user_json_response['user_id']
        user_get_response = requests.get(f"http://localhost:8000/user/{self.user_id}")
        user_get_json_response = json.loads(user_get_response.text)
        self.user_data['user_id'] = self.user_id
        self.assertEqual(user_get_response.status_code, 200)
        self.assertEqual(user_get_json_response, self.user_data)

    def UserTestPut(self):
        user_put_response = requests.put(f"http://localhost:8000/user/{self.user_id}",
                                         {'user_name': 'test_put'})
        self.assertEqual(user_put_response.status_code, 200)
        self.user_data['user_name'] = 'test_put'
        self.assertEqual(json.loads(user_put_response.text), self.user_data)

    def UserTestDelete(self):
        response = requests.delete(f'http://localhost:8000/user/{self.user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.text)['user_id'], None)

    def test_user(self):
        self.UserTestPost()
        self.UserTestPut()

    def tearDown(self) -> None:
        self.UserTestDelete()


class WebApp(APITestCase):
    def setUp(self):
        self.options = webdriver.ChromeOptions()
        self.driver_file = "/Users/adelgaraev/Downloads/chromedriver_mac64-2/chromedriver"
        self.browser = webdriver.Chrome(self.driver_file, options=self.options)
        self.browser.maximize_window()
        self.browser.implicitly_wait(10)
        self.browser.get('chrome://settings/')
        self.browser.execute_script('chrome.settingsPrivate.setDefaultZoom(0.8);')
        self.browser.get('http://localhost:9000')

        self.created_test_id = 0

    def login_in(self):
        button = self.browser.find_element(value="btn-login")
        ActionChains(self.browser).move_to_element(button).click().perform()
        time.sleep(2)
        self.assertEqual('http://localhost:9000/login', self.browser.current_url)

        login_input = self.browser.find_element(value='login')
        password_input = self.browser.find_element(value='password')

        login_input.send_keys("admin")
        password_input.send_keys("admin")

        log_in_button = self.browser.find_element(value="log-in-btn")
        ActionChains(self.browser).move_to_element(log_in_button).click().perform()

        time.sleep(2)
        current_user_name = self.browser.find_element(value="current-user-name").text
        self.assertEqual("http://localhost:9000/home", self.browser.current_url)
        self.assertEqual("Admin", current_user_name)

    def create_test(self):
        test_list_btn = self.browser.find_element(value="test-list-btn")
        ActionChains(self.browser).move_to_element(test_list_btn).click().perform()
        time.sleep(1)
        self.assertEqual("http://localhost:9000/tests", self.browser.current_url)

        self.browser.implicitly_wait(10)
        test_create_btn = self.browser.find_element(value='test-create-btn')
        ActionChains(self.browser).move_to_element(test_create_btn).click().perform()

        test_name_input = self.browser.find_element(value='test-name-input')
        test_subject_input = self.browser.find_element(value='test-subject-input')
        test_type_selector = self.browser.find_element(by=By.XPATH, value='//*[@id="test-type-select"]')
        test_name_input.send_keys("Тестовый тест")
        test_subject_input.send_keys("Тестовая дисциплина")
        test_type_selector.click()
        select = Select(test_type_selector)
        select.select_by_index(0)

        new_test_submit_btn = self.browser.find_element(by=By.XPATH,
                                                        value='//*[@id="test-modal___BV_modal_footer_"]/button[2]')
        new_test_submit_btn.click()

        test_table = self.browser.find_elements(by=By.XPATH, value='/html/body/div/div[2]/div/div/div/table/tbody/tr')
        name = self.browser.find_element(by=By.XPATH,
                                         value=f'/html/body/div/div[2]/div/div/div/table/tbody/'
                                               f'tr[{len(test_table)}]/td[2]')
        self.created_test_id = self.browser.find_element(by=By.XPATH,
                                                         value=f'/html/body/div/div[2]/div/div/div/table/'
                                                               f'tbody/tr[{len(test_table)}]/td[1]').text
        self.assertEqual('Тестовый тест', name.text)

    def constructor_test(self):
        test_table = self.browser.find_elements(by=By.XPATH, value='/html/body/div/div[2]/div/div/div/table/tbody/tr')
        new_test_id = self.browser.find_element(by=By.XPATH,
                                                value=f'/html/body/div/div[2]/div/div/div/table/tbody/'
                                                      f'tr[{len(test_table)}]/td[1]').text
        constructor_page_btn = self.browser.find_element(by=By.XPATH,
                                                         value=f'/html/body/div/div[2]/div/div/div/table/tbody/'
                                                               f'tr[{len(test_table)}]/td[8]/button')
        constructor_page_btn.click()
        self.assertEqual(f'http://localhost:9000/test/{new_test_id}', self.browser.current_url)

        new_q_add_btn = self.browser.find_element(by=By.XPATH,
                                                  value='/html/body/div/div[3]/table/thead/tr[1]/th[1]/button[1]')
        questions_table = self.browser.find_elements(by=By.XPATH,
                                                     value='/html/body/div/div[3]/table/tbody/tr')

        for i in range(3):
            new_q_add_btn.click()
            self.browser.implicitly_wait(10)
            question_text_input = self.browser.find_element(value='question-text-input')
            q_add_type_selector = Select(self.browser.find_element(value='q-type-selector'))
            new_q_save = self.browser.find_element(by=By.XPATH,
                                                   value='//*[@id="question-modal___BV_modal_footer_"]/button[1]')
            q_name = f'Вопрос {i + 1}'
            question_text_input.send_keys(q_name)
            q_add_type_selector.select_by_index(i)
            new_q_save.click()
            self.browser.implicitly_wait(5)

            added_question_text = self.browser.find_element(by=By.XPATH,
                                                            value=f'/html/body/div/div[3]/table/tbody/'
                                                                  f'tr[{i + 1}]/td[2]').text
            self.assertEqual(q_name, added_question_text)

        standard_q_edit_btn = self.browser.find_element(by=By.XPATH,
                                                        value='/html/body/div/div[3]/table/tbody/tr[1]/td[5]/button')
        standard_q_edit_btn.click()
        new_standard_answer_input = self.browser.find_element(value='new-standard-answer-input')
        new_standard_answer_checkbox = self.browser.find_element(by=By.XPATH,
                                                                 value='/html/body/div[2]/div[1]/'
                                                                       'div/div/div/div/form/div/label')
        new_standard_answer_btn = self.browser.find_element(value='new-standard-answer-btn')
        for i in range(2):
            new_standard_answer_input.send_keys(f'Ответ {i + 1}')
            if i == 0: new_standard_answer_checkbox.click()
            new_standard_answer_btn.click()
            time.sleep(0.5)
            # добавить проверку текста
        # добавить проверку количества вопросов
        self.browser.find_element(by=By.XPATH, value='/html/body/div[2]/div[1]/div/div/footer/button').click()
        time.sleep(0.5)

        while True:
            try:
                ActionChains(self.browser).scroll_by_amount(delta_x=0, delta_y=1).perform()
                comparison_q_edit_btn = self.browser.find_element(by=By.XPATH,
                                                                  value='/html/body/div/div[3]/table/tbody/tr[2]/td[5]/button')
                comparison_q_edit_btn.click()
                break
            except:
                continue
        open_answer_text = self.browser.find_element(by=By.XPATH,
                                                     value='/html/body/div[2]/div[1]/div/div/div/div/input').text
        self.assertEqual('Открытый ответ', open_answer_text)
        self.browser.find_element(by=By.XPATH, value='/html/body/div[2]/div[1]/div/div/footer/button').click()
        time.sleep(0.5)

        while True:
            try:
                comparison_q_edit_btn = self.browser.find_element(by=By.XPATH,
                                                                  value='/html/body/div/div[3]/table/tbody/tr[3]/td[5]/button')
                comparison_q_edit_btn.click()
                break
            except:
                ActionChains(self.browser).scroll_by_amount(delta_x=0, delta_y=1).perform()
                continue

        first_part_input = self.browser.find_element(by=By.XPATH,
                                                     value='/html/body/div[2]/div[1]/div/div/div/div/form/div/input[1]')
        second_part_input = self.browser.find_element(by=By.XPATH,
                                                      value='/html/body/div[2]/div[1]/div/div/div/div/form/div/input[2]')
        comparison_answer_add = self.browser.find_element(by=By.XPATH,
                                                          value='/html/body/div[2]/div[1]/div/div/div/div/form/div/button')
        comparison_data = [["Пушкин", "Евгений Онегин"], ["Тургенев", "Муму"]]

        for i in comparison_data:
            first_part_input.send_keys(i[0])
            second_part_input.send_keys(i[1])
            comparison_answer_add.click()
            time.sleep(0.5)

        self.browser.find_element(by=By.XPATH, value='/html/body/div[2]/div[1]/div/div/footer/button').click()
        time.sleep(0.5)

    def passing_test(self):
        while True:
            try:
                ActionChains(self.browser).scroll_by_amount(0, -1).perform()
                home_page_btn = self.browser.find_element(value='home-page-btn')
                home_page_btn.click()
                break
            except:
                continue
        self.assertEqual('http://localhost:9000/home', self.browser.current_url)

        self.browser.find_element(value='test-search-input').send_keys(self.created_test_id)
        self.browser.find_element(value='test-search-button').click()
        time.sleep(1)
        self.assertEqual(f'http://localhost:9000/test_view/{self.created_test_id}', self.browser.current_url)

        test_name = self.browser.find_element(by=By.XPATH, value='/html/body/div/div[2]/div/div[1]/h2').text
        self.assertEqual('Тестовый тест', test_name)

        self.browser.find_element(by=By.XPATH, value='/html/body/div/div[2]/div/div[2]/button').click()
        time.sleep(1)
        self.assertEqual(f'http://localhost:9000/passing/{self.created_test_id}', self.browser.current_url)

        self.browser.find_element(by=By.XPATH, value='/html/body/div/div[1]/div/div[1]/fieldset/div/div/div[1]/label')\
            .click()

        self.browser.find_element(by=By.XPATH, value='/html/body/div/div[1]/div/div[2]/fieldset/div/input')\
            .send_keys('Текст ответа')

        for i in range(2):
            answer_text = self.browser\
                .find_element(by=By.XPATH,
                              value=f'/html/body/div/div[1]/div/div[3]/fieldset/div/table/tbody/tr[{i+1}]/td[1]')\
                .text
            comparison_selector = Select(self.browser
                                         .find_element(by=By.XPATH,
                                                       value=f'/html/body/div/div[1]/div/div[3]/fieldset/div/table/'
                                                             f'tbody/tr[{i+1}]/td[2]/select'))
            if answer_text == 'Пушкин':
                comparison_selector.select_by_visible_text('Евгений Онегин')
            else:
                comparison_selector.select_by_visible_text('Муму')

        self.browser.find_element(by=By.XPATH, value='/html/body/div/button').click()
        self.browser.find_element(by=By.XPATH, value='/html/body/div[2]/div[1]/div/div/footer/button[2]').click()

        self.browser.implicitly_wait(10)
        percent = self.browser.find_element(by=By.XPATH, value='/html/body/div[2]/div[1]/div/div/div/div/p[2]').text
        self.assertEqual('100%', percent)

    def test_full(self):
        self.login_in()
        self.create_test()
        self.constructor_test()
        self.passing_test()

    def tearDown(self):
        # Добавить удаление созданного теста
        self.browser.quit()
