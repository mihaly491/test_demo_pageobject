from time import sleep
import pytest
from selenium import webdriver
from Pages.common import CommonObjects
from Pages.main_page import MainPage
from Pages.product_page import ProductPage
from Pages.checkout_page import CheckoutPage
from Pages.order_success_page import OrderSuccessPage
from Config.config import TestData


class TestAuthorization:
    def test_should_be_success_message_after_user_login_with_valid_name_and_password(self, driver):
        page = MainPage(driver, TestData.BASE_URL)
        page.open()
        page.login_with_name_and_password(TestData.USER_NAME, TestData.PASSWORD)
        page.should_be_text_in_alert_message(TestData.ALERT_MSG)


class TestGuestBuyProduct:

    def test_guest_can_see_cookie_alert(self, driver):
        page = MainPage(driver, TestData.BASE_URL)
        page.open()
        page.should_be_cookie_alert()

    def test_guest_can_open_product_page_from_main_page(self, driver):
        page = MainPage(driver, TestData.BASE_URL)
        page.open()
        page.accept_cookies()
        page.choose_product_from_product_area()

    def test_guest_can_add_product_to_cart(self, driver):
        page = MainPage(driver, TestData.BASE_URL)
        page.open()
        page.accept_cookies()
        page.choose_product_from_product_area()
        product_page = ProductPage(driver, TestData.BASE_URL)
        product_page.choose_size(TestData.PRODUCT_SIZE)
        product_page.add_to_cart()
        product_page.should_be_items_in_cart_badge()

    def test_guest_can_confirm_the_order(self, driver):
        page = MainPage(driver, TestData.BASE_URL)
        page.open()
        page.accept_cookies()
        page.choose_product_from_product_area()
        product_page = ProductPage(driver, TestData.BASE_URL)
        product_page.choose_size(TestData.PRODUCT_SIZE)
        product_page.add_to_cart()
        product_page.should_be_items_in_cart_badge()
        product_page.go_to_checkout_page()
        checkout_page = CheckoutPage(driver, TestData.BASE_URL)
        checkout_page.fill_in_required_fields()
        checkout_page.save_changes()
        checkout_page.confirm_order()
        order_success_page = OrderSuccessPage(driver, TestData.BASE_URL)
        order_success_page.should_be_text_in_confirm_message(TestData.ORDER_CONFIRMED_MSG)
        order_success_page.should_be_selected_product_in_item_list(TestData.PRODUCT)

class TestAuthorizedUserBuyProduct:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, driver):
        link = TestData.BASE_URL
        page = MainPage(driver, link)
        page.open()
        page.login_with_name_and_password(TestData.USER_NAME, TestData.PASSWORD)

        yield

        link = TestData.BASE_URL + "/logout"
        page = MainPage(driver, link)
        page.open()

    def test_user_can_open_product_page_from_main_page(self, driver):
        page = MainPage(driver, TestData.BASE_URL)
        page.open()
        page.accept_cookies()
        page.choose_product_from_product_area()

    def test_user_can_confirm_the_order(self, driver):
        page = MainPage(driver, TestData.BASE_URL)
        page.open()
        page.accept_cookies()
        page.choose_product_from_product_area()
        product_page = ProductPage(driver, TestData.BASE_URL)
        product_page.open()
        product_page.choose_size(TestData.PRODUCT_SIZE)
        product_page.add_to_cart()
        product_page.should_be_items_in_cart_badge()
        product_page.go_to_checkout_page()
        checkout_page = CheckoutPage(driver, TestData.BASE_URL)
        checkout_page.open()
        checkout_page.confirm_order()
        order_success_page = OrderSuccessPage(driver, TestData.BASE_URL)
        order_success_page.should_be_text_in_confirm_message(TestData.ORDER_CONFIRMED_MSG)
        order_success_page.should_be_selected_product_in_item_list(TestData.PRODUCT)