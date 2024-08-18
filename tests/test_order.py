import allure
import pytest
from api.order import Order
from conftest import created_courier
import helpers.generate_order_data as helper


@allure.epic('API testing of Yandex.Scooter. Test cases for orders')
class TestCreateOrder:
    @allure.title('Create order using correct data')
    @pytest.mark.parametrize('color', (['BLACK'], ['GREY'], ['BLACK', 'GREY'], ''))
    def test_create_order_success(self, color: list):
        order = Order()
        order_data = helper.generate_order_data(color)
        response = order.create_order(order_data)
        assert response.status_code == 201 and 'track' in response.json()

class TestAcceptOrder:
    @allure.title('Accept an order with a correct ID')
    def test_accept_order_success(self, created_courier):
        order = Order()
        order_data = helper.generate_order_data(['BLACK'])
        order.create_order(order_data)
        order_id = order.get_order_id()
        courier_id = created_courier.get_courier_id()
        response = order.accept_order(order_id, courier_id)
        assert response.status_code == 200 and response.json() == {'ok': True}

    @allure.title('Accept an order with a missing ID')
    def test_accept_order_missing_order_failure(self, created_courier):
        order = Order()
        order_data = helper.generate_order_data(['BLACK'])
        order.create_order(order_data)
        courier_id = created_courier.get_courier_id()
        order_id = 111111111
        response = order.accept_order(order_id=order_id, courier_id=courier_id)
        assert response.status_code == 404 and response.json()['message'] == "Заказа с таким id не существует"

    @allure.title('Accept an order by a courier with a missing ID')
    def test_accept_order_missing_courier_failure(self, created_courier):
        order = Order()
        order_data = helper.generate_order_data(['BLACK'])
        order.create_order(order_data)
        courier_id = 123456789
        order_id = order.get_order_track_num()
        response = order.accept_order(order_id, courier_id)
        assert response.status_code == 404 and response.json()['message'] == "Курьера с таким id не существует"

    @allure.title('Accept an order by a courier with void ID')
    def test_accept_order_void_courier_id_failure(self, created_courier):
        order = Order()
        order_data = helper.generate_order_data(['BLACK'])
        order.create_order(order_data)
        courier_id = ''
        order_id = order.get_order_id()
        response = order.accept_order(order_id, courier_id)
        assert response.status_code == 400 and response.json()['message'] == "Недостаточно данных для поиска"

    @allure.title('Accept an order already being processed')
    def test_accept_processed_order_failure(self, created_courier):
        order = Order()
        order_data = helper.generate_order_data(['BLACK'])
        order.create_order(order_data)
        courier_id = created_courier.get_courier_id()
        order_id = 100
        response = order.accept_order(order_id, courier_id)
        assert response.status_code == 409 and response.json()['message'] == "Этот заказ уже в работе"


class TestGetOrdersList:
    @allure.title('Get orders list')
    def test_get_orders_list_success(self):
        response = Order.get_list_of_orders()
        assert response.status_code == 200


class TestGetOrdersInfo:
    @allure.title('Get an order info by a correct track number')
    def test_get_order_by_num_success(self):
        order = Order()
        order_data = helper.generate_order_data(['BLACK'])
        order.create_order(order_data)
        order_num = order.get_order_track_num()
        response = order.get_order_by_track_num(order_num)
        assert response.status_code == 200 and 'order' in response.json()

    @allure.title('Get an order info using a void track number')
    def test_get_order_void_num_failure(self):
        response = Order().get_order_by_track_num('')
        assert response.status_code == 400 and response.json()['message'] == 'Недостаточно данных для поиска'

    @allure.title('Get an order info using a missing track number')
    def test_get_order_missing_num_failure(self):
        response = Order().get_order_by_track_num(1)
        assert response.status_code == 404 and response.json()['message'] == 'Заказ не найден'
