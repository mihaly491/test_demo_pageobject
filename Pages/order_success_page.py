from selenium.webdriver.common.by import By
from Base.base_page import BasePage
from Config.config import TestData
from Pages.locators import OrderSuccessPageLocators

class OrderSuccessPage(BasePage):

    def should_be_text_in_confirm_message(self, text):
        assert text in self.get_element_text(OrderSuccessPageLocators.ORDER_CONFIRMED_MSG), \
            "Text not found, order failed"

    def should_be_selected_product_in_item_list(self, product):
        assert product in self.get_element_text(OrderSuccessPageLocators.ITEM_LIST), \
            "No selected item found in item list"
