import allure
import requests
import helpers.endpoints as url


class Order:

    def __init__(self):
        self.track_num = None
        self.id = None
        self.data = {}

    @allure.step('Create an order')
    def create_order(self, data):
        url_create_order = f"{url.BASE_URL}{url.CREATE_ORDER}"
        response = requests.post(url_create_order, json=data)
        self.track_num = response.json()['track']
        self.data = self.get_order_by_track_num(self.track_num)
        self.id = self.get_order_id_by_track_num(self.data)
        return response

    @staticmethod
    @allure.step('Get an orders list')
    def get_list_of_orders():
        url_order_list = f"{url.BASE_URL}{url.ORDER_LIST}"
        return requests.get(url_order_list)

    @allure.step('Accept an order by a courier')
    def accept_order(self, order_id, courier_id):
        url_accept_order = f"{url.BASE_URL}{url.ACCEPT_ORDER}/{order_id}?courierId={courier_id}"
        print(url_accept_order)
        return requests.put(url_accept_order, timeout=40)

    @allure.step('Cancel an order')
    def cancel_order(self, order_id):
        url_cancel_order = f"{url.BASE_URL}{url.CANCEL_ORDER}/{order_id}"
        data = {'track': order_id}
        return requests.put(url_cancel_order, data=data)

    @allure.step('Get an order by a track number')
    def get_order_by_track_num(self, order_track_num):
        url_get_order = f"{url.BASE_URL}{url.GET_ORDER_BY_ID}?t={order_track_num}"
        return requests.get(url_get_order)

    @allure.step('Get an order ID by a track number')
    def get_order_id_by_track_num(self, data):
        return data.json()['order']['id']

    @allure.step('Get an order ID')
    def get_order_id(self):
        if self.id:
            return self.id
        return None

    @allure.step('Get an order track number')
    def get_order_track_num(self):
        if self.track_num:
            return self.track_num
        return None
