from Config.config import TestData
from itertools import product
from Pages.common import CommonObjects
from Pages.main_page import MainPage
from Pages.product_page import ProductPage
from Pages.checkout_page import CheckoutPage
from Pages.order_success_page import OrderSuccessPage
import allure
import pytest
from selenium import webdriver
from time import sleep


@allure.feature("Проверка авторизации")
@allure.story("Гость может авторизоваться под своим логином и паролем")
class TestAuthorization:
    @allure.title("Успешная авторизация с валидными данными")
    @allure.description("Проверяет, что после входа отображается сообщение об успешной авторизации")
    def test_should_be_success_message_after_user_login_with_valid_name_and_password(self, driver):
        page = MainPage(driver, TestData.BASE_URL)
        page.open()
        with allure.step("Ввести логин, пароль и авторизоваться"):
            page.login_with_name_and_password(TestData.USER_NAME, TestData.PASSWORD)
        sleep(1)
        with allure.step("Проверить наличие сообщения об успешной авторизации"):
            page.should_be_text_in_alert_message(TestData.ALERT_MSG)

@allure.feature("Оформление заказа гостем")
class TestGuestBuyProduct:

    @allure.story("Гость может увидеть уведомление о cookies")
    @allure.title("Проверка появления cookie-alert на главной странице")
    def test_guest_can_see_cookie_alert(self, driver):
        page = MainPage(driver, TestData.BASE_URL)
        page.open()
        sleep(1)
        with allure.step("Проверить, что отображается предупреждение о cookies"):
            page.should_be_cookie_alert()

    @allure.story("Гость может открыть страницу товара")
    @allure.title("Переход со страницы каталога на страницу товара")
    def test_guest_can_open_product_page_from_main_page(self, driver):
        page = MainPage(driver, TestData.BASE_URL)
        page.open()
        page.accept_cookies()
        sleep(1)
        with allure.step(f"Выбрать товар '{TestData.BASE_URL}' из блока товаров"):
            page.choose_product_from_product_area(TestData.PRODUCT)

    @allure.story("Гость может добавить товар в корзину")
    @allure.title("Добавление выбранного товара в корзину")
    def test_guest_can_add_product_to_cart(self, driver):
        page = MainPage(driver, TestData.BASE_URL)
        page.open()
        page.accept_cookies()
        page.choose_product_from_product_area(TestData.PRODUCT)
        product_page = ProductPage(driver, TestData.BASE_URL)
        product_page.choose_size(TestData.PRODUCT_SIZE)
        with allure.step("Добавить товар в корзину"):
            product_page.add_to_cart()
        sleep(1)
        with allure.step("Проверить, что отображается значок количества товаров"):
            product_page.should_be_items_in_cart_badge()

    @allure.story("Гость может оформить заказ")
    @allure.title("Полный сценарий покупки товара гостем")
    def test_guest_can_confirm_the_order(self, driver):
        with allure.step("Открыть сайт и выбрать товар из блока товаров"):
            page = MainPage(driver, TestData.BASE_URL)
            page.open()
            page.accept_cookies()
            page.choose_product_from_product_area(TestData.PRODUCT)

        with allure.step("Добавить товар в корзину"):
            product_page = ProductPage(driver, TestData.BASE_URL)
            product_page.choose_size(TestData.PRODUCT_SIZE)
            product_page.add_to_cart()
            product_page.should_be_items_in_cart_badge()

        with allure.step("Оформить заказ"):
            product_page.go_to_checkout_page()
            checkout_page = CheckoutPage(driver, TestData.BASE_URL)
            checkout_page.fill_in_required_fields()
            checkout_page.save_changes()
            checkout_page.confirm_order()

        with allure.step("Проверить успешное подтверждение заказа"):
            order_success_page = OrderSuccessPage(driver, TestData.BASE_URL)
            sleep(1)
            order_success_page.should_be_text_in_confirm_message(TestData.ORDER_CONFIRMED_MSG)
            order_success_page.should_be_selected_product_in_item_list(TestData.PRODUCT)

    @pytest.mark.parametrize("product_name,size", [
        (p, s) if p in TestData.PRODUCTS_WITH_SIZES else (p, None)
        for p in TestData.PRODUCTS
        for s in (TestData.PRODUCT_SIZES if p in TestData.PRODUCTS_WITH_SIZES else [None])
    ])
    @allure.story("Гость может оформить заказ на все доступные товары")
    @allure.title("Покупка {product_name} (размер: {size}")
    def test_guest_can_buy_all_products_from_product_area(self, driver, product_name, size):
        with allure.step("Открыть страницу и выбрать товар из блока товаров"):
            page = MainPage(driver, TestData.BASE_URL)
            page.open()
            page.accept_cookies()
            page.choose_product_from_product_area(product_name)

        with allure.step("Добавить товар в корзину"):
            product_page = ProductPage(driver, TestData.BASE_URL)
            if size:
                product_page.choose_size(size)
            product_page.add_to_cart()
            product_page.should_be_items_in_cart_badge()
            product_page.go_to_checkout_page()

        with allure.step("Оформить заказ"):
            checkout_page = CheckoutPage(driver, TestData.BASE_URL)
            checkout_page.fill_in_required_fields()
            checkout_page.save_changes()
            checkout_page.confirm_order()

        with allure.step("Проверить сообщение об успешном заказе"):
            order_success_page = OrderSuccessPage(driver, TestData.BASE_URL)
            sleep(1)
            order_success_page.should_be_text_in_confirm_message(TestData.ORDER_CONFIRMED_MSG)
            order_success_page.should_be_selected_product_in_item_list(product_name)

@allure.feature("Покупка авторизованным пользователем")
class TestAuthorizedUserBuyProduct:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, driver):
        link = TestData.BASE_URL
        page = MainPage(driver, link)
        page.open()
        page.accept_cookies()
        with allure.step("Авторизация пользователя"):
            page.login_with_name_and_password(TestData.USER_NAME, TestData.PASSWORD)

        yield

        with allure.step("Выход из аккаунта"):
            link = TestData.BASE_URL + "/logout"
            page = MainPage(driver, link)
            page.open()

    @allure.story("Авторизованный пользователь может открыть страницу товара")
    def test_user_can_open_product_page_from_main_page(self, driver):
        page = MainPage(driver, TestData.BASE_URL)
        page.open()
        sleep(1)
        with allure.step(f"Выбрать товар '{TestData.PRODUCT}'"):
            page.choose_product_from_product_area(TestData.PRODUCT)

    @allure.story("Авторизованный пользователь может оформить заказ")
    def test_user_can_confirm_the_order(self, driver):
        with allure.step("Выбрать товар с главной страницы"):
            page = MainPage(driver, TestData.BASE_URL)
            page.open()
            page.choose_product_from_product_area(TestData.PRODUCT)

        with allure.step("Добавить товар в корзину"):
            product_page = ProductPage(driver, TestData.BASE_URL)
            product_page.choose_size(TestData.PRODUCT_SIZE)
            product_page.add_to_cart()
            product_page.should_be_items_in_cart_badge()

        with allure.step("Подтвердить заказ"):
            product_page.go_to_checkout_page()
            checkout_page = CheckoutPage(driver, TestData.BASE_URL)
            checkout_page.confirm_order()

        with allure.step("Проверить сообщение об успешном заказе"):
            order_success_page = OrderSuccessPage(driver, TestData.BASE_URL)
            sleep(1)
            order_success_page.should_be_text_in_confirm_message(TestData.ORDER_CONFIRMED_MSG)
            order_success_page.should_be_selected_product_in_item_list(TestData.PRODUCT)

    @pytest.mark.parametrize("product_name,size", [
        (p, s) if p in TestData.PRODUCTS_WITH_SIZES else (p, None)
        for p in TestData.PRODUCTS
        for s in (TestData.PRODUCT_SIZES if p in TestData.PRODUCTS_WITH_SIZES else [None])
    ])
    @allure.story("Авторизованный пользователь может оформить заказ на все доступные товары")
    @allure.title("Покупка {product_name} (размер: {size}")
    def test_user_can_buy_all_products_from_product_area(self, driver, product_name, size):
        with allure.step("Выбрать товар с главной страницы"):
            page = MainPage(driver, TestData.BASE_URL)
            page.choose_product_from_product_area(product_name)

        with allure.step("Добавить товар в корзину"):
            product_page = ProductPage(driver, TestData.BASE_URL)
            if size:
                product_page.choose_size(size)
            product_page.add_to_cart()
            product_page.should_be_items_in_cart_badge()
            product_page.go_to_checkout_page()

        with allure.step("Подтвердить заказ"):
            checkout_page = CheckoutPage(driver, TestData.BASE_URL)
            checkout_page.confirm_order()

        with allure.step("Проверить сообщение об успешном заказе"):
            order_success_page = OrderSuccessPage(driver, TestData.BASE_URL)
            sleep(1)
            order_success_page.should_be_text_in_confirm_message(TestData.ORDER_CONFIRMED_MSG)
            order_success_page.should_be_selected_product_in_item_list(product_name)