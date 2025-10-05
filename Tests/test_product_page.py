from time import sleep
import pytest
from selenium import webdriver
from Pages.common import CommonObjects
from Pages.main_page import MainPage
from Pages.product_page import ProductPage
from Pages.checkout_page import CheckoutPage
from Pages.order_success_page import OrderSuccessPage
from Config.config import TestData


class TestGuestBuyProduct:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, driver):
        link = TestData.BASE_URL

    def test_guest_can_see_cookie_alert(self, driver):
        page = MainPage(driver, TestData.BASE_URL)
        page.open()
        page.should_be_cookie_alert()

    def test_guest_can_open_product_page_from_main_page(self, driver):
        page = MainPage(driver, TestData.BASE_URL)
        page.open()
        page.accept_cookies()
        page.choose_product_from_product_area()


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

