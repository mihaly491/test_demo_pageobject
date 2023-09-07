from selenium.webdriver.common.by import By
from Base.BasePage import BasePage
from Config.config import TestData


class OrderSuccessPage(BasePage):

    ORDER_CONFIRMED_MSG = (By.CLASS_NAME, "card-title")

    def __init__(self, driver):
        super().__init__(driver)

    def check_that_confirm_msg_contains_text(self, text):
        assert text in self.get_element_text(self.ORDER_CONFIRMED_MSG)