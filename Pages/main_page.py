import time

from selenium.webdriver.common.by import By
from Base.base_page import BasePage
from Config.config import TestData
from Pages.locators import BasePageLocators
from Pages.locators import MainPageLocators


class MainPage(BasePage):

    def __init__(self, *args, **kwargs):
        super(MainPage, self).__init__(*args, **kwargs)

    def should_be_text_in_alert_message(self, text):
        assert text in self.get_element_text(MainPageLocators.ALERT_MSG), f"Text {text} not found in alert message"

    def choose_product_from_product_area(self):
        self.scroll_to_element(MainPageLocators.PRODUCT_AREA)
        self.do_click(MainPageLocators.PRODUCT_IMAGE)
