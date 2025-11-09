import allure
from selenium.webdriver.common.by import By
from Base.base_page import BasePage
from Config.config import TestData
from Pages.locators import OrderSuccessPageLocators

class OrderSuccessPage(BasePage):

    def __init__(self, driver, url):
        super().__init__(driver, url)
        self.wait_for_page_stability()

    @allure.step("Проверка текста подтверждения заказа")
    def should_be_text_in_confirm_message(self, expected_text):
        actual_text = self.get_element_text(OrderSuccessPageLocators.ORDER_CONFIRMED_MSG)
        self.assert_contains(expected_text, actual_text, "Проверка текста подтверждения заказа")

    @allure.step("Ппроверка наличия выбранного товара в заказе")
    def should_be_selected_product_in_item_list(self, product):
        actual_items = self.get_element_text(OrderSuccessPageLocators.ITEM_LIST)
        self.assert_contains(product, actual_items, "Проверка, что товар '{product}' присутствует в заказе")

    @allure.step("Перейти на версию для печати")
    def go_to_order_printable_copy_page(self):
        self.do_click(OrderSuccessPageLocators.PRINTABLE_COPY_BUTTON)