import time

from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver):
        self.driver = driver

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

    def is_present(self, by_locator):
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(by_locator))
        return bool(element)

    def get_title(self, title):
        WebDriverWait(self.driver, 10).until(EC.title_is(title))
        return self.driver.title

    def wait_for_element_to_load(self, by_locator):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator))

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
                break
            else:
                continue

    def get_list_items(self, by_locator):
        items = Select(WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(by_locator)))
        return items
