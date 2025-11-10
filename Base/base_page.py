import time

from selenium.common import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from Pages.locators import BasePageLocators
import allure


class BasePage:

    def __init__(self, driver, url):
        self.driver = driver
        self.url = url
        self.wait_for_page_stability()

    @staticmethod
    def log_step(action: str, by_locator=None, extra: str = ""):
        if by_locator:
            by, value = by_locator
            step_text = f"{action}: {by} → {value}"
        else:
            step_text = action
        if extra:
            step_text += f" [{extra}]"

        with allure.step(step_text):
            pass

    def assert_with_allure(self, condition, expected, actual, message="Проверка условия"):
        allure.attach(
            f"Ожидаемый результат: {expected}\nФактический результат: {actual}",
            name=f"Результат проверки — {message}",
            attachment_type=allure.attachment_type.TEXT
        )

        if not condition:
            try:
                allure.attach(
                    self.driver.get_screenshot_as_png(),
                    name="Скриншот при ошибке",
                    attachment_type=allure.attachment_type.PNG
                )
                allure.attach(
                    self.driver.page_source,
                    name="HTML страницы при ошибке",
                    attachment_type=allure.attachment_type.HTML
                )
            except Exception as e:
                print(f"[Allure] Не удалось прикрепить дополнительные материалы: {e}")

        assert condition, f"{message}\nОжидаемый результат: {expected}\nФактический результат: {actual}"

    def assert_equals(self, expected, actual, message="Проверка равенства"):
        self.assert_with_allure(expected == actual, expected, actual, message)

    def assert_contains(self, expected_substring, actual, message="Проверка содержимого"):
        self.assert_with_allure(expected_substring in actual, expected_substring, actual, message)

    def open(self):
        self.log_step(f"Открыть страницу {self.url}")
        self.driver.get(self.url)
        self.driver.maximize_window()
        self.wait_for_page_stability()

    def switch_to_new_tab(self):
        self.log_step(f"Переключиться на другую вкладку")
        handles = self.driver.window_handles
        if len(handles) > 1:
            self.driver.switch_to.window(handles[-1])
        else:
            raise AssertionError("No new tab found to switch to!")

    def wait_for_page_stability(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return jQuery.active == 0")
            )
        except Exception:
            pass

    def do_click(self, by_locator):
        self.log_step("Клик по элементу", by_locator)
        element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(by_locator))
        element.click()
        self.wait_for_page_stability()

    def do_clear(self, by_locator):
        self.log_step("Очистить поле", by_locator)
        element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(by_locator))
        element.clear()
        self.wait_for_page_stability()

    def do_send_keys(self, by_locator, text):
        self.log_step("Ввод текста", by_locator, extra=text)
        element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(by_locator))
        element.send_keys(text)
        self.wait_for_page_stability()

    def get_element_text(self, by_locator):
        self.log_step("Получение текста элемента", by_locator)
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator))
        text = element.text.strip()

        with allure.step(f"Текст элемента: {text[:50]}..."):
            pass

        allure.attach(
            text,
            name=f"Текст элемента {by_locator[1]}",
            attachment_type=allure.attachment_type.TEXT
        )

        return text

    def get_elements_text(self, by_locator):
        self.log_step("Получение текста из списка элементов", by_locator)
        elements = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located(by_locator))
        texts = [el.text.strip() for el in elements if el.text.strip()]

        allure.attach(
            "\n".join(texts),
            name=f"Список найденныхх элементов ({len(texts)})",
            attachment_type=allure.attachment_type.TEXT
        )
        return texts

    def get_element_value(self, by_locator):
        self.log_step("Получение значения из поля", by_locator)
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator))
        value = element.get_attribute("value")

        allure.attach(
            str(value),
            name=f"Значение элемента {by_locator[1]}",
            attachment_type=allure.attachment_type.TEXT
        )

        return value

    def is_enabled(self, by_locator):
        self.log_step("Проверить доступность элемента", by_locator)
        try:
            WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(by_locator))
            return True
        except TimeoutException:
            return False

    def is_element_present(self, by_locator, timeout=5):
        self.log_step("Проверка присутствия элемента", by_locator)
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(by_locator))
            return True
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
            return False

    def is_not_element_present(self, by_locator, timeout=5):
        self.log_step("Проверка отсутствия элемента", by_locator)
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(by_locator))
        except TimeoutException:
            return True

    def get_page_title(self, title):
        WebDriverWait(self.driver, 10).until(EC.title_is(title))
        return self.driver.title


    def wait_for_element(self, by_locator, timeout=10):
        self.log_step("Дождаться появления элемента", by_locator)
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(by_locator))
            return element
        except TimeoutException:
            raise AssertionError(f"Element {by_locator} not found at {timeout} seconds")

    def scroll_to_element(self, by_locator):
        self.log_step("Прокрутка страницы до элемента", by_locator)
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
        self.log_step("Получить все значения из списка", by_locator)
        items = Select(WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(by_locator)))
        return items

    def get_list_item_text(self, by_locator):
        self.log_step("Получить значение из списка", by_locator)
        select_object = Select(WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(by_locator)))
        selected_option = select_object.first_selected_option
        return selected_option.text

    def login_with_name_and_password(self, username: str, password: str):
        self.log_step("Ввести логин, пароль и авторизоваться", (username, password))
        self.do_click(BasePageLocators.SIGNUP_NAV_BTN)
        self.do_clear(BasePageLocators.EMAIL_INPUT)
        self.do_clear(BasePageLocators.PASSWORD_INPUT)
        self.do_send_keys(BasePageLocators.EMAIL_INPUT, username)
        self.do_send_keys(BasePageLocators.PASSWORD_INPUT, password)
        self.do_click(BasePageLocators.LOGIN_BTN)

    def should_be_cookie_alert(self):
        self.log_step("Проверить, что отображается предупреждение о cookies")
        assert self.is_element_present(BasePageLocators.COOKIE_NOTICE), "User doesn't see cookie alert"

    def accept_cookies(self):
        self.log_step("Принять cookies")
        if self.is_element_present(BasePageLocators.COOKIE_NOTICE):
            self.do_click(BasePageLocators.ACCEPT_COOKIES_BTN)

    def go_to_checkout_page(self):
        self.log_step("Перейти на страницу оформления заказа")
        self.do_click(BasePageLocators.CART)

    def go_to_main_page(self):
        self.log_step("Перейти на главную страницу")
        self.do_click(BasePageLocators.SITE_LOGO)