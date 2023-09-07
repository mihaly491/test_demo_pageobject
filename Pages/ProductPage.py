from selenium.webdriver.common.by import By
from Base.BasePage import BasePage
from Config.config import TestData


class ProductPage(BasePage):

    PRODUCT_TITLE = (By.CSS_SELECTOR, "h1.title")
    SIZE_OPTION = (By.CSS_SELECTOR, "select.form-control[name=\"options[Size]\"]")
    ADD_TO_CART_BTN = (By.NAME, "add_cart_product")
    CART_BADGE = (By.CSS_SELECTOR, "#cart .badge")

    def __init__(self, driver):
        super().__init__(driver)

    def choose_size(self, option):
        self.do_click(self.SIZE_OPTION)
        options = self.get_list_items(self.SIZE_OPTION)
        options.select_by_visible_text(option)

    def add_to_cart(self):
        self.do_click(self.ADD_TO_CART_BTN)

    def check_cart_badge_has_items(self, text):
        assert text in self.get_element_text(self.CART_BADGE)
