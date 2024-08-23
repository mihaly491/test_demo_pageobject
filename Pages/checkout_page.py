from selenium.webdriver.common.by import By
from Base.base_page import BasePage
from Config.config import TestData
from Pages.locators import CheckoutPageLocators


class CheckoutPage(BasePage):

    def __init__(self, driver, url):
        super().__init__(driver, url)
        self.item_price = None

    def should_be_items_in_cart(self):
        assert CheckoutPageLocators.CHECKOUT_CART in CheckoutPageLocators.CHECKOUT_WRAPPER

    def should_be_required_item_in_cart(self, item):
        assert item in CheckoutPageLocators.CHECKOUT_CART

    def get_item_price(self):
        self.item_price = self.get_element_text(CheckoutPageLocators.ITEM_PRICE).strip().replace("$", "")

    def confirm_order(self):
        self.do_click(CheckoutPageLocators.CHECKBOX_TERMS_AGREED)
        self.do_click(CheckoutPageLocators.CONFIRM_ORDER_BTN)
