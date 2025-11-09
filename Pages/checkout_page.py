from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from Base.base_page import BasePage
from Config.config import TestData
from Pages.locators import CheckoutPageLocators
from faker import Faker
import allure


class CheckoutPage(BasePage):

    def __init__(self, driver, url):
        super().__init__(driver, url)
        self.item_price = None
        self.wait_for_page_stability()
        self._entered_data = {}

    def get_entered_data(self, element):
        return self._entered_data[element]

    def set_entered_data(self, element, value):
        self._entered_data[element] = value

    @allure.step("Проверить наличие товаров в корзине")
    def should_be_items_in_cart(self):
        assert CheckoutPageLocators.CHECKOUT_CART in CheckoutPageLocators.CHECKOUT_WRAPPER

    def should_be_required_item_in_cart(self, item):
        assert item in CheckoutPageLocators.CHECKOUT_CART

    @allure.step("Проверить цену товара")
    def get_item_price(self):
        self.item_price = self.get_element_text(CheckoutPageLocators.ITEM_PRICE).strip().replace("$", "")

    def get_country(self):
        country_code_select = Select(self.driver.find_element(*CheckoutPageLocators.COUNTRY_CODE_SELECT))
        return country_code_select.first_selected_option.text

    @allure.step("Заполнить обязательные поля")
    def fill_in_required_fields(self):
        faker = Faker()

        self.do_send_keys(CheckoutPageLocators.FIRSTNAME_INPUT, faker.first_name())
        self.do_send_keys(CheckoutPageLocators.LASTNAME_INPUT, faker.last_name())
        self.do_send_keys(CheckoutPageLocators.ADDRESS1_INPUT, faker.address())
        self.do_send_keys(CheckoutPageLocators.POSTALCODE_INPUT, faker.postalcode())
        self.do_send_keys(CheckoutPageLocators.CITY_INPUT, faker.city())
        self.get_list_items(CheckoutPageLocators.COUNTRY_CODE_SELECT).select_by_visible_text("United States")
        # self.get_list_items(CheckoutPageLocators.ZONE_CODE_SELECT).select_by_visible_text("Alabama")
        self.do_send_keys(CheckoutPageLocators.EMAIL_INPUT, faker.email())
        self.do_send_keys(CheckoutPageLocators.PHONE_INPUT, "1234567")

    @allure.step("Запомнить введёные данные в карточке")
    def save_checkout_data(self):
        self.set_entered_data('company', self.get_element_value(CheckoutPageLocators.COMPANY_INPUT))
        self.set_entered_data('first_name', self.get_element_value(CheckoutPageLocators.FIRSTNAME_INPUT))
        self.set_entered_data('last_name', self.get_element_value(CheckoutPageLocators.LASTNAME_INPUT))
        self.set_entered_data('address1', self.get_element_value(CheckoutPageLocators.ADDRESS1_INPUT))
        self.set_entered_data('address2', self.get_element_value(CheckoutPageLocators.ADDRESS2_INPUT))
        self.set_entered_data('postalcode', self.get_element_value(CheckoutPageLocators.POSTALCODE_INPUT))
        self.set_entered_data('city', self.get_element_value(CheckoutPageLocators.CITY_INPUT))
        self.set_entered_data('country', self.get_list_item_text(CheckoutPageLocators.COUNTRY_CODE_SELECT))
        self.set_entered_data('email', self.get_element_value(CheckoutPageLocators.EMAIL_INPUT))
        self.set_entered_data('phone', self.get_element_value(CheckoutPageLocators.PHONE_INPUT))

    @allure.step("Загрузить ранее введённые данные в карточке")
    def load_checkout_data(self):
        return {
            'company': self.get_entered_data('company'),
            'first_name': self.get_entered_data('first_name'),
            'last_name': self.get_entered_data('last_name'),
            'address1': self.get_entered_data('address1'),
            'address2': self.get_entered_data('address2'),
            'postalcode': self.get_entered_data('postalcode'),
            'city': self.get_entered_data('city'),
            'country': self.get_entered_data('country'),
            'email': self.get_entered_data('email'),
            'phone': self.get_entered_data('phone')
        }

    @allure.step("Сохранить изменения")
    def save_changes(self):
        self.do_click(CheckoutPageLocators.SAVE_CHANGES_BTN)

    @allure.step("Подтвердить заказ")
    def confirm_order(self):
        self.do_click(CheckoutPageLocators.CHECKBOX_TERMS_AGREED)
        self.do_click(CheckoutPageLocators.CONFIRM_ORDER_BTN)
