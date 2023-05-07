from utilities.compare_visual import expect_to_have_screenshot
from tests.test_base import BaseTest
from selenium.webdriver.common.by import By
import allure
import pytest


@allure.story('Login functionality')
class TestLogin(BaseTest):
    @allure.description("Visual testing login page, should fail")
    @allure.title('Visual testing login page, should fail')
    @pytest.mark.Visual
    def test_visual_login_fail(self,request):
        self.nav_bar.click_login_icon()
        #This to make the test fail
        if(request.config.getoption("--update-snapshot")==False):
            element =self.driver.find_element(By.XPATH, "//*[contains(text(), 'Log in or register with your mobile number')]")
            self.driver.execute_script("arguments[0].textContent = 'New text value';", element)
        assert expect_to_have_screenshot(request,self.driver)

    @allure.description("Visual testing login page, should pass")
    @allure.title('Visual testing login page, should pass')
    @pytest.mark.Visual
    def test_visual_login_pass(self,request):
        masked_element = {(By.XPATH, "//div[contains(@class, 'latest__left')]"),(By.XPATH, "//div[contains(@class, 'latest__right')]")}
        self.nav_bar.click_login_icon()
        assert expect_to_have_screenshot(request,self.driver,masked_locators=masked_element)==True    
       
