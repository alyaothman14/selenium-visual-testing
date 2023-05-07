import os
from selenium.webdriver import Chrome,Firefox
from typing import Union, List,Tuple
from pixelmatch.contrib.PIL import pixelmatch
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
import pytest
import time
import allure

'''
Utility to check for screenshot difference
request: test request context
driver
threshold: allowed threshold for image difference, default 0.1
masked_locator: list of locator tuple that should be masked in the screenshot
z-index: z-index for the mask default 2000
full_screenshot: take a full screenshot, default false

Return True or False
Raise an exception if there is a pixel difference
'''
def expect_to_have_screenshot(request: pytest.FixtureRequest,driver:Union[Chrome, Firefox],**kwargs)-> bool:
    test_name=request.node.name
    directory= f'{request.node.fspath.dirname}/{request.node.fspath.purebasename}'
    update_snapshot = request.config.getoption("--update-snapshot")
    expected_snapshot_location= f'{directory}/{test_name}-baseline.png'
    actual_snapshot_location= f'{directory}/{test_name}-actual.png'
    diff_snapshot_location=f'{directory}/{test_name}-diff.png'
    threshold=kwargs.get('threshold', 0.1)

    if os.path.exists(actual_snapshot_location):
        os.remove(actual_snapshot_location)
    if os.path.exists(diff_snapshot_location):
        os.remove(diff_snapshot_location)    
    if not os.path.isfile(expected_snapshot_location) and not update_snapshot:
        raise Exception("Baseline screenshot does not exist. Please run the command with --update-snapshot")
    wait_for_network_ideal(driver)
    if 'masked_locators' in kwargs:
        z_index='2000' if not 'z-index' in kwargs else kwargs["z-index"]
        mask_element(kwargs['masked_locators'],driver,z_index) 
    if update_snapshot:
        allure.step("Take baseline snapshot")
        if not os.path.exists(directory):
            os.makedirs(directory)
        if os.path.exists(expected_snapshot_location):
            os.remove(expected_snapshot_location)    
        if('full_screenshot' in kwargs):
            driver.save_full_page_screenshot(expected_snapshot_location)
            return True
        else:
            driver.save_screenshot(expected_snapshot_location)
            return True
   
    if('full_screenshot' in kwargs):
        driver.save_full_page_screenshot(actual_snapshot_location)
    else:
        driver.save_screenshot(actual_snapshot_location)
    if not update_snapshot:                
        expected_image= Image.open(expected_snapshot_location).convert('RGBA')
        actual_image= Image.open(actual_snapshot_location).convert('RGBA')
        diff_image = Image.new("RGBA", expected_image.size)
        allure.step("Comparing screenshots")
        diff_pixels= pixelmatch(expected_image,actual_image,diff_image,threshold)
        if diff_pixels>threshold:
            diff_image.save(diff_snapshot_location)
            raise Exception(f"{diff_pixels} pixels differ from the expected result")

        return True

def mask_element(locators_list: List[Tuple[By, str]],driver:Union[Chrome, Firefox],z_index:str):
    wait= WebDriverWait(driver,30)
    for locator in locators_list:
        element: WebElement = wait.until(
                expected_conditions.visibility_of_element_located(locator))
        x= element.location['x']
        y= element.location['y']
        width=element.size['width']
        height= element.size['height']
        js_code = f"""
            var canvas = document.createElement('canvas');
            canvas.width = {width};
            canvas.height = {height};
            canvas.style.position = 'absolute';
            canvas.style.left = '{x}px';
            canvas.style.top = '{y}px';
            canvas.style.zIndex = '{z_index}';
            canvas.style.pointerEvents = 'none';
            document.body.appendChild(canvas);
            var ctx = canvas.getContext('2d');
            ctx.fillStyle = 'rgba(255, 0, 255, 1)';
            ctx.fillRect(0, 0, {width}, {height});
            """
        driver.execute_script(js_code)

def wait_for_network_ideal(driver:Union[Chrome, Firefox]):
    wait = WebDriverWait(driver, 30)
    wait.until(expected_conditions.presence_of_element_located((By.TAG_NAME, 'body')))
    network_ideal=False
    retry=0
    network_count=driver.execute_script('return window.performance.getEntriesByType("resource").length')
    while(not network_ideal or not retry==3 ):
        time.sleep(5)
        current_count=driver.execute_script('return window.performance.getEntriesByType("resource").length')
        if(network_count==current_count):
            break
        else:
            network_count=current_count
            retry=retry+1
            time.sleep(5)

    

    


