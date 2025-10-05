from selenium.webdriver.common.by import By
from Base.base_page import BasePage
from Config.config import TestData


class CommonObjects(BasePage):

    def __init__(self, driver, url):
        super().__init__(driver, url)
