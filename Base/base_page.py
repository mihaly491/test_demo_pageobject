import time

from selenium.common import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from Pages.locators import BasePageLocators


class BasePage:

    def __init__(self, driver, url, timeout=10):
        self.driver = driver
        self.url = url
        self.driver.implicitly_wait(timeout)

    def open(self):
        self.driver.get(self.url)
        self.driver.maximize_window()

    def do_click(self, by_locator):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator)).click()

    def do_clear(self, by_locator):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator)).clear()

    def do_send_keys(self, by_locator, text):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator)).send_keys(text)

    def get_element_text(self, by_locator):
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator))
        return element.text

    def is_enabled(self, by_locator):
        try:
            WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(by_locator))
            return True
        except TimeoutException:
            return False

    def is_element_present(self, how, what, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((how, what)))
            return True
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
            return False

    def is_not_element_present(self, how, what, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return True

    def get_page_title(self, title):
        WebDriverWait(self.driver, 10).until(EC.title_is(title))
        return self.driver.title

    def wait_for_element(self, how, what, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((how, what)))
            return element
        except TimeoutException:
            raise AssertionError(f"Element {what} not found at {how} seconds")


    def scroll_to_element(self, by_locator):
        actions = ActionChains(self.driver)
        element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(by_locator))
        actions.move_to_element(element)
        actions.perform()

    def find_element_from_set_by_alt(self, by_locator, element):
        els = set(WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(by_locator)))

        for el in els:
            if el.get_attribute("alt") == element:
                return el
            else:
                continue

    def get_list_items(self, by_locator):
        items = Select(WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(by_locator)))
        return items

    def login_with_name_and_password(self, username: str, password: str):
        self.do_click(BasePageLocators.SIGNUP_NAV_BTN)
        self.do_clear(BasePageLocators.EMAIL_INPUT)
        self.do_clear(BasePageLocators.PASSWORD_INPUT)
        self.do_send_keys(BasePageLocators.EMAIL_INPUT, username)
        self.do_send_keys(BasePageLocators.PASSWORD_INPUT, password)
        self.do_click(BasePageLocators.LOGIN_BTN)

    def should_be_cookie_alert(self):
        assert self.is_element_present(*BasePageLocators.COOKIE_NOTICE), "User doesn't see cookie alert"

    def accept_cookies(self):
        if self.is_element_present(*BasePageLocators.COOKIE_NOTICE):
            self.do_click(BasePageLocators.ACCEPT_COOKIES_BTN)

    def go_to_checkout_page(self):
        self.do_click(BasePageLocators.CART)
