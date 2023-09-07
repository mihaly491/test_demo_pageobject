import time

from selenium.webdriver.common.by import By
from Base.BasePage import BasePage
from Config.config import TestData


class MainPage(BasePage):

    EMAIL = (By.NAME, "email")
    PASSWORD = (By.NAME, "password")
    SIGNUP_NAV_BTN = (By.CSS_SELECTOR, "li.nav-item.account.dropdown > a")
    LOGIN_BTN = (By.NAME, "login")
    COOKIE_NOTICE = (By.ID, "box-cookie-notice")
    ACCEPT_COOKIES_BTN = (By.NAME, "accept_cookies")
    ALERT_MSG = (By.CSS_SELECTOR, ".alert.alert-success")
    PRODUCT_AREA = (By.CSS_SELECTOR, "article.product")
    PRODUCT_BOX = (By.CSS_SELECTOR, "article.product img")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get(TestData.BASE_URL)
        self.driver.maximize_window()

    def login_with_name_and_password(self, username: str, password: str):
        self.do_click(self.SIGNUP_NAV_BTN)
        self.do_clear(self.EMAIL)
        self.do_clear(self.PASSWORD)
        self.do_send_keys(self.EMAIL, username)
        self.do_send_keys(self.PASSWORD, password)
        self.do_click(self.LOGIN_BTN)

    def accept_cookies(self):
        if self.is_present(self.COOKIE_NOTICE):
            self.do_click(self.ACCEPT_COOKIES_BTN)

    def check_that_alert_msg_contains_text(self, text):
        assert text in self.get_element_text(self.ALERT_MSG)

    def choose_product(self, product):
        self.scroll_to_element(self.PRODUCT_AREA)
        selected_product = self.find_element_from_set_by_alt(self.PRODUCT_BOX, product)
        selected_product.click()
