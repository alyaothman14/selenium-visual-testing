from typing import Union
from selenium.webdriver import Chrome, Firefox
import pytest


from pages.nav_bar_page import SportyNavBarPage


@pytest.mark.usefixtures("setup")
class BaseTest:
    driver: Union[Chrome, Firefox]
    nav_bar: SportyNavBarPage
    browser: str
