from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import pytest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from pages.nav_bar_page import SportyNavBarPage
import allure
import os

from utilities.compare_visual import wait_for_network_ideal
# read command line options
# allow to define browser
# To run only one browser pass -k "chrome"


def pytest_addoption(parser:pytest.Parser):
    parser.addoption("--update-snapshot", action="store",default=False, help="update snapshot for visual testing")

def pytest_generate_tests(metafunc):
    browsers = ["chrome", "firefox"]
    if "browser" in metafunc.fixturenames:
        metafunc.parametrize("browser", browsers)


@pytest.fixture(scope="function")
def setup(request: pytest.FixtureRequest, browser):
    if (browser in ("chrome")):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.set_capability(
            "goog:loggingPrefs", {"browser": "ALL"}
        )

    match browser:
        case "chrome":
            chrome_options.headless = True
            driver = webdriver.Chrome(service=ChromeService(
                ChromeDriverManager().install()), options=chrome_options)
            driver.maximize_window()
        case "firefox":
            firefox_options = webdriver.FirefoxOptions()
            firefox_options.headless = True
            driver = webdriver.Firefox(service=FirefoxService(
                GeckoDriverManager().install()), options=firefox_options)
            driver.maximize_window()
    driver.get("https://sporty.com/news/latest")
    # make sure the page is loaded
    wait = WebDriverWait(driver, 30)
    wait.until(expected_conditions.visibility_of_element_located(
        ((By.XPATH, "//*[contains(text(),'Customise your')]"))))
    wait_for_network_ideal(driver)
    request.cls.driver = driver
    request.cls.nav_bar = SportyNavBarPage(driver)
    yield driver
    allure.dynamic.tag(driver.capabilities["browserName"])
    test_name=request.node.name
    directory= f'{request.node.fspath.dirname}/{request.node.fspath.purebasename}'
    diff_snapshot_location=f'{directory}/{test_name}-diff.png'
    expected_snapshot_location= f'{directory}/{test_name}-baseline.png'
    actual_snapshot_location= f'{directory}/{test_name}-actual.png'
    if os.path.exists(diff_snapshot_location):
        with allure.step("Visual comparison"):
            allure.attach.file(expected_snapshot_location, name="Expected screenshot", attachment_type=allure.attachment_type.PNG)
            allure.attach.file(actual_snapshot_location, name="Actual screenshot", attachment_type=allure.attachment_type.PNG)
            allure.attach.file(diff_snapshot_location, name="Visual diff", attachment_type=allure.attachment_type.PNG)

    driver.quit()
