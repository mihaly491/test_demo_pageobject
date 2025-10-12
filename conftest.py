from requests.compat import has_simplejson
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
import allure
import pytest
import platform
import os
import sys


def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store", default="chrome", help="Choose browser Chrome, Firefox, or Edge")


def setup_driver_service(browser_name):
    try:
        if browser_name == "chrome":
            return ChromeService(ChromeDriverManager().install())
        elif browser_name == "firefox":
            return FirefoxService(GeckoDriverManager().install())
        elif browser_name == "edge":
            return EdgeService(EdgeChromiumDriverManager().install())
    except Exception as e:
        print(f"WebDriver Manager failed: {e}")
        return setup_driver_manual(browser_name)


def setup_driver_manual(browser_name):
    system = platform.system().lower()

    driver_paths = {
        'windows': {
            'chrome': 'C:/chromedriver-win32/chromedriver.exe',
            'firefox': 'C:/geckodriver/geckodriver.exe',
            'edge': 'C:/edgedriver/msedgedriver.exe'
        },
        'linux': {
            'chrome': '/usr/local/bin/chromedriver',
            'firefox': '/usr/local/bin/geckodriver',
            'edge': '/usr/local/bin/msedgedriver'
        }
    }

    path = driver_paths.get(system, {}).get(browser_name)
    if path and os.path.exists(path):
        if browser_name == "chrome":
            return ChromeService(executable_path=path)
        elif browser_name == "firefox":
            return FirefoxService(executable_path=path)
        elif browser_name == "edge":
            return EdgeService(executable_path=path)

    raise Exception(f"Driver for {browser_name} not found on {system}")


@pytest.fixture(scope="function")
def driver(request):
    browser_name = request.config.getoption("browser_name")

    print(f"\nStarting {browser_name} browser on {platform.system()}..")

    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        if platform.system().lower() == 'linux':
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
    elif browser_name == "edge":
        options = webdriver.EdgeOptions()
        options.add_argument("--guest")

    # Настройка сервиса
    service = setup_driver_service(browser_name)

    # Создание драйвера
    if browser_name == "chrome":
        driver = webdriver.Chrome(service=service, options=options)
    elif browser_name == "firefox":
        driver = webdriver.Firefox(service=service, options=options)
    elif browser_name == "edge":
        driver = webdriver.Edge(service=service, options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    allure.dynamic.parameter("Browser", browser_name)

    if hasattr(request.node, "callspec"):
        for name, value  in request.node.callspec.params.items():
            allure.dynamic.parameter(name, value)

    yield driver

    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        try:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot on failure",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception as e:
            print(f"[Allure attachment failed] Screenshot not captured: {e}")


        try:
            allure.attach(
                driver.page_source,
                name="HTML page source",
                attachment_type=allure.attachment_type.HTML,
            )
        except Exception as e:
            print(f"[Allure attachment failed] HTML not captured: {e}")

    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)

import pytest
import platform
import sys
import allure
import os


def pytest_configure(config):

    env_dir = os.path.join(os.getcwd(), "allure-results")
    os.makedirs(env_dir, exist_ok=True)

    browser_name = config.getoption("--browser_name")

    env_properties = {
        "Browser": browser_name,
        "Platform": platform.system(),
        "Platform-Version": platform.version(),
        "Python-Version": sys.version.split()[0],
        "Pytest-Version": pytest.__version__,
        "Allure-Version": allure.__version__ if hasattr(allure, "__version__") else "N/A",
    }

    env_file_path = os.path.join(env_dir, "environment.properties")

    with open(env_file_path, "w", encoding="utf-8") as f:
        for key, value in env_properties.items():
            f.write(f"{key}={value}\n")

    print(f"[Allure] Environment info written to {env_file_path}")
