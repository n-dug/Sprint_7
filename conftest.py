import pytest

from api.courier import Courier


@pytest.fixture()
def created_courier():
    courier = Courier()
    courier.create_courier()
    yield courier
    courier.delete_courier(courier.get_courier_id())
