import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store", default="chrome", help="Choose browser Chrome, Firefox, or Edge")


@pytest.fixture(scope="session")
def driver(request):
    # Open driver and set up URL and window
    chrome_options = ChromeOptions()
    firefox_options = FirefoxOptions()
    firefox_options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"
    edge_options = webdriver.EdgeOptions()
    edge_options.add_argument("--guest")

    chrome_service = ChromeService(executable_path="C:/chromedriver-win32/chromedriver.exe", log_path="chromedriver.log")
    firefox_service = FirefoxService(executable_path="C:/geckodriver/geckodriver.exe", log_path="geckodriver.log")

    browser_name = request.config.getoption("browser_name")
    driver = None
    if browser_name == "chrome":
        print("\nStart chrome browser for test..")
        driver = webdriver.Chrome(options=chrome_options, service=chrome_service)
    # elif browser_name == "firefox":
    #     print("\nStart firefox browser for test..")
    #     driver = webdriver.Firefox(options=firefox_options, service=firefox_service)
    # elif browser_name == "edge":
    #     print("\nStart edge browser for test..")
    #     driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=edge_options)

    # Close driver when tests done
    yield driver
    driver.quit()
