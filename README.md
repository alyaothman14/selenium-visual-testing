# Selenium with Python and Allure on GitHub

The project setup visual testing for Selenium using pixelmatch libary
The project does the following 
- update baseline snapshot if update-snapshot label is added to the PR and commit the snapshot to the PR
- Run visual testing and compare screenshots, attach difference to allure report
- There is an example of failing testcase to see how it looks in allure report
- The utility allows to mask certain locator to get stable snapshot in case of dynamic content

## Project Setup

1. Install Allure:
```bash
brew install allure
```
2. Install the required Python packages:
```bash
pip install
```
3. Run the tests using one of the following commands:
```bash
pipenv run pytest -k "chrome" to run chrome only
pipenv run pytest -k "firefox" to run firefox only
pipenv run pytest to run all
```
4. Generate the Allure report:
```bash
allure serve
```

#Use visual testing
```bash
 assert expect_to_have_screenshot(request,self.driver)
 ```
 If you need to mask an element the utility accept list of locators
 ```bash
  masked_element = {(By.XPATH, "//div[contains(@class, 'latest__left')]"),(By.XPATH, "//div[contains(@class, 'latest__right')]")}
        self.nav_bar.click_login_icon()
        assert expect_to_have_screenshot(request,self.driver,masked_locators=masked_element)==True    
  ``` 


#You can find the allure results [here](https://alyaothman14.github.io/selenium-python/visual/)

#Example of Commit:
Snapshot Commit from pipeline [here](https://github.com/alyaothman14/selenium-visual-testing/pull/1/commits/67642b526ccce1592cd717eda5b83e3a8cb2f1ee)

#Example of Difference in report
![image](https://user-images.githubusercontent.com/87079479/236699643-9885c5e7-134b-4ff7-a126-28a2310b6eb7.png)

#Ideas for improvement:
- Overlay the actual and expected image with a slider in the report to be easy to see the difference
- Only commit the snapshot if there is a change between the new updated snapshot and the baseline

