from selenium.webdriver.common.by import By
from Base.BasePage import BasePage
from Config.config import TestData


class CommonObjects(BasePage):

    SEARCH = (By.NAME, "query")
    REGIONAL_SETTINGS = (By.CLASS_NAME, "regional-setting")
    ACCOUNT = (By.CLASS_NAME, "account")
    CART = (By.ID, "cart")

    def __init__(self, driver):
        super().__init__(driver)

