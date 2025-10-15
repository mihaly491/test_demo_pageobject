from selenium.webdriver.common.by import By
from Base.base_page import BasePage
from Config.config import TestData
from Pages.locators import OrderSuccessPageLocators

class OrderSuccessPage(BasePage):

    def __init__(self, driver, url):
        super().__init__(driver, url)
        self.wait_for_page_stability()

    def should_be_text_in_confirm_message(self, text):
        actual_text = self.get_element_text(OrderSuccessPageLocators.ORDER_CONFIRMED_MSG)
        assert text in actual_text, f"Text not found: expected '{text}', got '{actual_text}'"

    def should_be_selected_product_in_item_list(self, product):
        items_text = self.get_element_text(OrderSuccessPageLocators.ITEM_LIST)
        assert product in items_text, f"No selected item '{product}' found in item list: '{items_text}'"
