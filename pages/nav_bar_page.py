"""
This defines the login page components
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from typing import Union, Tuple
from selenium.webdriver import Chrome, Firefox
import allure


class SportyNavBarPage(BasePage):

    LOGIN_ICON: Tuple[By, str] = (By.XPATH, "//*[contains(text(),'Log In')]")
    LOGGED_IN_USER: Tuple[By, str] = (By.XPATH, "//*[contains(text(),'Hi,')]")

    def __init__(self, driver: Union[Chrome, Firefox]):
        super().__init__(driver)

    @allure.step("User clicks login icon in nav bar")
    def click_login_icon(self) -> None:
        self.click(self.LOGIN_ICON)

    @allure.step("Return username when user logged in")
    def get_user_name(self) -> str:
        return self.get_text(self.LOGGED_IN_USER)
   # TODO: Add login for new user with verification code
