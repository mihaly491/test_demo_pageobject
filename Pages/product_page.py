import allure
from selenium.webdriver.common.by import By
from Base.base_page import BasePage
from Config.config import TestData
from Pages.locators import ProductPageLocators


class ProductPage(BasePage):

    def __init__(self, driver, url):
        super().__init__(driver, url)
        self.wait_for_page_stability()

    @allure.step("Проверить возможность выбрать размер товара")
    def should_be_size_select(self):
        assert self.is_element_present(*ProductPageLocators.SIZE_OPTION)

    @allure.step("Выбрать размер товара: {option}")
    def choose_size(self, option):
        if not self.is_element_present(*ProductPageLocators.SIZE_OPTION):
            return

        self.do_click(ProductPageLocators.SIZE_OPTION)
        options = self.get_list_items(ProductPageLocators.SIZE_OPTION)
        options.select_by_visible_text(option)

    @allure.step("Перейти в корзину")
    def add_to_cart(self):
        self.do_click(ProductPageLocators.ADD_TO_CART_BTN)

    @allure.step("Проверить, что значок корзины отображает добавленные товары")
    def should_be_items_in_cart_badge(self):
        cart_badge_quantity = self.get_element_text(ProductPageLocators.CART_BADGE)
        assert cart_badge_quantity != "", "Cart badge not found. Have the product added to cart?"
