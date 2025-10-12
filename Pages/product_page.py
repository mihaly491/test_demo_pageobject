import allure
from selenium.webdriver.common.by import By
from Base.base_page import BasePage
from Config.config import TestData
from Pages.locators import ProductPageLocators


class ProductPage(BasePage):

    def should_be_size_select(self):
        assert self.is_element_present(*ProductPageLocators.SIZE_OPTION)

    def choose_size(self, option):
        if not self.is_element_present(*ProductPageLocators.SIZE_OPTION):
            return

        self.do_click(ProductPageLocators.SIZE_OPTION)
        options = self.get_list_items(ProductPageLocators.SIZE_OPTION)
        options.select_by_visible_text(option)

    def add_to_cart(self):
        self.do_click(ProductPageLocators.ADD_TO_CART_BTN)

    def should_be_items_in_cart_badge(self):
        cart_badge_quantity = self.get_element_text(ProductPageLocators.CART_BADGE)
        assert cart_badge_quantity != "", "Cart badge not found. Have the product added to cart?"
