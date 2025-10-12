# test_demo_pageobject

Test data in Config/config.py

Run test_main_page.py

conftest.py is used to set up Selenium driver.

Use https://googlechromelabs.github.io/chrome-for-testing/#stable for chromedriver and https://github.com/mozilla/geckodriver/releases for geckodriver

Run with `pytest --alluredir=allure-results`

Generate report with `allure serve allure-results`