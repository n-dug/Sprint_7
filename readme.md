Итоговый проект 7 спринта.
Структура проекта:
allure_results - каталог с отчетами allure
tests/test_order.py - тесты на ручки "Создать заказ", "Показать список заказов"
tests/test_courier.py - тесты на ручки "Создать курьера", "Логин курьера"
conftest.py - фикстуры
helpers/endpoints.py - файл с URL
helpers/generate_order_data.py - файл с генератором данных о заказе
requirements.txt - файл с внешними зависимостями
api/courier.py - файл с методами, которые вызываются в тестах функциональности курьеров.
api/order.py - файл с методами, которые вызываются в тестах функциональности заказов.