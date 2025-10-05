import pytest
from selenium import webdriver
from test_demo_pageobject.Pages.mainpage import MainPage
from test_demo_pageobject.Config.config import TestData


@pytest.fixture
def driver():
    # Open driver and set up URL and window
    driver = webdriver.Chrome()

    # Close driver when tests done
    yield driver
    driver.quit()


def test_when_login_with_valid_name_and_password_success_message_should_appear(driver):
    mainpage = MainPage(driver)
    mainpage.login_with_name_and_password(TestData.USER_NAME, TestData.PASSWORD)
    mainpage.check_that_alert_msg_contains_text(TestData.ALERT_MSG)
