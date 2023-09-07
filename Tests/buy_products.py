import pytest
from selenium import webdriver
from Pages.common import CommonObjects
from Pages.MainPage import MainPage
from Pages.ProductPage import ProductPage
from Pages.CheckoutPage import CheckoutPage
from Pages.OrderSuccessPage import OrderSuccessPage
from Config.config import TestData


def test_buy_product(driver):
    mainpage = MainPage(driver)
    productpage = ProductPage(driver)
    checkoutpage = CheckoutPage(driver)
    ordersuccesspage = OrderSuccessPage(driver)

    mainpage.login_with_name_and_password(TestData.USER_NAME, TestData.PASSWORD)
    mainpage.accept_cookies()
    mainpage.choose_product(TestData.PRODUCT)

    if productpage.is_enabled(productpage.SIZE_OPTION) == True:
        productpage.choose_size(TestData.PRODUCT_SIZE)

    productpage.add_to_cart()
    productpage.wait_for_element_to_load(productpage.CART_BADGE)

    checkoutpage.open()
    checkoutpage.confirm_order()

    ordersuccesspage.check_that_confirm_msg_contains_text(TestData.ORDER_CONFIRMED_MSG)
