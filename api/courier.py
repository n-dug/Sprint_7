import allure
import random
import requests
import string
import helpers.endpoints as url


class Courier:
    def __init__(self):
        self.data = None
        self.account_id = None

    @allure.step('Generate a courier data')
    def __generate_courier_data(self):
        def generate_random_string(length):
            letters = string.ascii_lowercase
            random_string = ''.join(random.choice(letters) for _ in range(length))
            return random_string
        data = {}
        login = generate_random_string(10)
        password = generate_random_string(10)
        name = generate_random_string(10)
        data["login"] = login
        data["password"] = password
        data["name"] = name
        return data

    @allure.step('Get a courier login')
    def get_login(self):
        return self.data['login']

    @allure.step('Get a courier password')
    def get_password(self):
        return self.data['password']

    @allure.step('Get a courier name')
    def get_name(self):
        return self.data['name']

    @allure.step('Get a courier data')
    def get_account_data(self):
        return self.data

    @allure.step('Create a courier')
    def create_courier(self, login: str = '', password: str = '', name: str = ''):
        if login == '' and password == '' and name == '':
            self.data = self.__generate_courier_data()
        response = requests.post(f"{url.BASE_URL}{url.CREATE_COURIER}", json=self.data)
        return response

    @allure.step('Login as a courier')
    def login_courier(self, login: str = '', password: str = ''):
        if login == '' and password == '':
            data = {
                "login": self.get_login(),
                "password": self.get_password(),
            }
        else:
            data = {
                "login": login,
                "password": password
            }
        return requests.post(f"{url.BASE_URL}{url.LOGIN_COURIER}", json=data)

    @allure.step('Delete a courier')
    def delete_courier(self, courier_id=None):
        return requests.delete(f"{url.BASE_URL}{url.DELETE_COURIER}/{courier_id}")

    @allure.step('Get a courier ID')
    def get_courier_id(self, login='', password=''):
        if login == '' and password == '':
            self.data = {
                "login": self.get_login(),
                "password": self.get_password(),
            }
        else:
            self.data = {
                "login": login,
                "password": password
            }
        response = self.login_courier(self.get_login(), self.get_password())
        if response.status_code == 200 and self.account_id is None:
            self.account_id = response.json().get('id')
            return self.account_id
        return -1
