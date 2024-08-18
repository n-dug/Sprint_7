import allure
import pytest
from api.courier import Courier
from conftest import created_courier, courier_delete_after_use


@allure.epic('API testing of Yandex.Scooter. Test cases for couriers')
class TestSignUpCourier:
    @allure.title('Sign up using correct data')
    def test_create_courier_success(self, courier_delete_after_use):
        courier_delete_after_use = Courier()
        response = courier_delete_after_use.create_courier()
        assert response.status_code == 201 and response.json() == {'ok': True}

    @allure.title('Sign up using duplicated data')
    def test_create_duplicated_courier_failure(self, created_courier):
        response = created_courier.create_courier(
            created_courier.get_login(), created_courier.get_password(), created_courier.get_name())
        assert response.status_code == 409 and response.json().get(
            'message') == 'Этот логин уже используется. Попробуйте другой.'

    @allure.title('Sign up without login or password')
    @pytest.mark.parametrize("key", ["login", "password"])
    def test_create_courier_without_login_or_password_failed(self, courier_delete_after_use, key):
        courier_delete_after_use = Courier()
        courier_delete_after_use.create_courier()
        creds = courier_delete_after_use.get_account_data()
        creds[key] = ''
        response = courier_delete_after_use.create_courier(creds)
        assert response.status_code == 400 and response.json().get(
            'message') == 'Недостаточно данных для создания учетной записи'

    @allure.title('Sign up without name')
    def test_create_courier_without_name_success(self, courier_delete_after_use):
        courier_delete_after_use = Courier()
        courier_delete_after_use.create_courier()
        creds = courier_delete_after_use.get_account_data()
        creds['name'] = ''
        response = courier_delete_after_use.create_courier(creds)
        assert (response.status_code == 409 and response.json().get('message') ==
                'Этот логин уже используется. Попробуйте другой.')


class TestSignInCourier:
    @allure.title('Sign in using correct data')
    def test_login_courier_success(self, created_courier):
        response = created_courier.login_courier()
        created_courier.account_id = response.json().get('id')
        assert response.status_code == 200 and created_courier.account_id is not None

    @allure.title('Sign in without login or password')
    @pytest.mark.parametrize("key", ("login", "password"))
    def test_login_without_login_or_password_failure(self, created_courier, key):
        created_courier.data[key] = ''
        response = created_courier.login_courier()
        assert response.status_code == 400 and response.json().get('message') == 'Недостаточно данных для входа'

    @allure.title('Sign in using incorrect login or password')
    @pytest.mark.parametrize("key", ("login", "password"))
    def test_login_with_wrong_credentials_failure(self, created_courier, key):
        created_courier.data[key] = 'Unknown'
        response = created_courier.login_courier()
        assert response.status_code == 404 and response.json().get('message') == 'Учетная запись не найдена'


class TestDeleteCourier:
    @allure.title('Delete courier with a correct ID')
    def test_delete_courier_success(self):
        courier = Courier()
        courier.create_courier()
        response = courier.delete_courier(courier.get_courier_id())
        assert response.status_code == 200 and response.json() == {'ok': True}

    @allure.title('Delete courier with incorrect ID')
    def test_delete_courier_with_incorrect_id(self, courier_delete_after_use):
        courier_delete_after_use = Courier()
        response = courier_delete_after_use.delete_courier(666)
        assert response.status_code == 404
        assert response.json()['message'] == 'Курьера с таким id нет.'
