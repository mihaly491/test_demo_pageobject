import pytest
from selenium import webdriver
from test_demo_pageobject.Pages.common import CommonObjects
from test_demo_pageobject.Pages.mainpage import MainPage
from test_demo_pageobject.Pages.productpage import ProductPage
from test_demo_pageobject.Pages.checkoutpage import CheckoutPage
from test_demo_pageobject.Pages.ordersuccesspage import OrderSuccessPage
from test_demo_pageobject.Config.config import TestData


@pytest.fixture
def driver():
    # Open driver and set up URL and window
    driver = webdriver.Chrome()

    # Close driver when tests done
    yield driver
    driver.quit()


def test_buy_small_yellow_duck(driver):
    mainpage = MainPage(driver)
    productpage = ProductPage(driver)
    checkoutpage = CheckoutPage(driver)
    ordersuccesspage = OrderSuccessPage(driver)

    mainpage.login_with_name_and_password(TestData.USER_NAME, TestData.PASSWORD)
    mainpage.choose_yellow_duck()

    productpage.choose_size(TestData.Sizes.SMALL)
    productpage.add_to_cart()

    checkoutpage.open()
    checkoutpage.wait_for_element_to_load(checkoutpage.CHECKOUT_CART)
    checkoutpage.confirm_order()

    ordersuccesspage.check_that_confirm_msg_contains_text(TestData.ORDER_CONFIRMED_MSG)

