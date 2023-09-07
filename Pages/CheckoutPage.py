from selenium.webdriver.common.by import By
from Base.BasePage import BasePage
from Config.config import TestData


class CheckoutPage(BasePage):

    CHECKOUT_WRAPPER = (By.CLASS_NAME, "cart wrapper")
    CHECKOUT_CART = (By.ID, "box-checkout-cart")
    CHECKOUT_CART_ITEMS = (By.CSS_SELECTOR, "#box-checkout-cart .items")
    CHECKBOX_TERMS_AGREED = (By.NAME, "terms_agreed")
    CONFIRM_ORDER_BTN = (By.NAME, "confirm_order")

    def __init__(self, driver):
        super().__init__(driver)

    def open(self):
        self.driver.get(TestData.SHOPPINGCART_URL)

    def check_that_cart_has_items(self):
        assert self.CHECKOUT_CART in self.CHECKOUT_WRAPPER

    def confirm_order(self):
        self.do_click(self.CHECKBOX_TERMS_AGREED)
        self.do_click(self.CONFIRM_ORDER_BTN)
