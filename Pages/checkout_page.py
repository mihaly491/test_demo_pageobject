from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from Base.base_page import BasePage
from Config.config import TestData
from Pages.locators import CheckoutPageLocators
from faker import Faker
from time import sleep


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

    def get_country(self):
        country_code_select = Select(self.driver.find_element(*CheckoutPageLocators.COUNTRY_CODE_SELECT))
        return country_code_select.first_selected_option.text

    def fill_in_required_fields(self):
        f = Faker('en_US')

        self.do_send_keys(CheckoutPageLocators.FIRSTNAME_INPUT, f.first_name())
        self.do_send_keys(CheckoutPageLocators.LASTNAME_INPUT, f.last_name())
        self.do_send_keys(CheckoutPageLocators.ADDRESS1_INPUT, f.address())
        self.do_send_keys(CheckoutPageLocators.POSTALCODE_INPUT, f.postalcode())
        self.do_send_keys(CheckoutPageLocators.CITY_INPUT, f.city())
        self.get_list_items(CheckoutPageLocators.COUNTRY_CODE_SELECT).select_by_visible_text("United States")
        # self.get_list_items(CheckoutPageLocators.ZONE_CODE_SELECT).select_by_visible_text("Alabama")
        self.do_send_keys(CheckoutPageLocators.EMAIL_INPUT, f.email())
        self.do_send_keys(CheckoutPageLocators.PHONE_INPUT, "1234567")

    def save_changes(self):
        self.do_click(CheckoutPageLocators.SAVE_CHANGES_BTN)

    def confirm_order(self):
        self.do_click(CheckoutPageLocators.CHECKBOX_TERMS_AGREED)
        self.do_click(CheckoutPageLocators.CONFIRM_ORDER_BTN)
