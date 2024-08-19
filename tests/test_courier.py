import allure
import pytest
from conftest import created_courier
import helpers.endpoints as url


@allure.epic('API testing of Yandex.Scooter. Test cases for couriers')
class TestSignUpCourier:
    @allure.title('Sign up using correct data')
    def test_create_courier_success(self, created_courier):
        response = created_courier.create_courier()
        assert response.status_code == 201 and response.json() == {'ok': True}

    @allure.title('Sign up using duplicated data')
    def test_create_duplicated_courier_failure(self, created_courier):
        response = created_courier.create_courier(
            created_courier.get_login(), created_courier.get_password(), created_courier.get_name())
        assert response.status_code == 409 and response.json().get(
            'message') == url.TEXT_LOGIN_EXISTS_409

    @allure.title('Sign up without login or password')
    @pytest.mark.parametrize("key", ["login", "password"])
    def test_create_courier_without_login_or_password_failure(self, created_courier, key):
        created_courier.data[key] = None
        response = created_courier.create_courier(name="NoLoginPass")
        assert response.status_code == 400 and response.json().get(
            'message') == url.TEXT_NOT_ENOUGH_CREDENTIALS_SIGN_UP_400

    @allure.title('Sign up without name')
    def test_create_courier_without_name_success(self, created_courier):
        created_courier.data['name'] = None
        response = created_courier.create_courier()
        assert response.status_code == 201 and response.json() == {'ok': True}


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
        assert (response.status_code == 400 and response.json().get('message')
                == url.TEXT_NOT_ENOUGH_CREDENTIALS_SIGN_IN_400)

    @allure.title('Sign in using incorrect login or password')
    @pytest.mark.parametrize("key", ("login", "password"))
    def test_login_with_wrong_credentials_failure(self, created_courier, key):
        created_courier.data[key] = 'Unknown'
        response = created_courier.login_courier()
        assert response.status_code == 404 and response.json().get('message') == url.TEXT_ACCOUNT_NOT_FOUND_404


class TestDeleteCourier:
    @allure.title('Delete courier with a correct ID')
    def test_delete_courier_success(self, created_courier):
        response = created_courier.delete_courier(created_courier.get_courier_id())
        assert response.status_code == 200 and response.json() == {'ok': True}

    @allure.title('Delete courier with incorrect ID')
    def test_delete_courier_with_incorrect_id(self, created_courier):
        response = created_courier.delete_courier(666)
        assert response.status_code == 404
        assert response.json()['message'] == url.TEXT_NO_COURIER_WITH_ID_404
