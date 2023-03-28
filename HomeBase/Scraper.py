from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
import time

from selenium.webdriver.chrome.options import Options


class User:
    userName = 'davidcastillo07@yahoo.com'
    password = 'Swagmaster2000'


# When Created, this opens a chrome window and logs in.
class HomeBaseBrowser:
    driver = None
    user = User()

    def __init__(self):
        if self.driver is None:
            chromeOptions = Options()
            chromeOptions.add_argument('--headless')
            self.driver = webdriver.Chrome(chrome_options=chromeOptions)
            self.driver.get('https://app.joinhomebase.com/schedule_builder')
            self.userName = 'davidcastillo07@yahoo.com'
            self.password = 'Swagmaster2000'
            self.login()

    def nextWeek(self):
        nextButton = '/html/body/div[1]/div/div[6]/div[1]/div/div/div[1]/div/section[1]/a[2]'
        self.driver.find_element_by_xpath(nextButton).click()

        loadMeDiv = '/html/body/div[1]/div/div[6]/div[1]/div/div/div[2]/div[2]/table[2]/tbody[7]/tr/td[5]'
        self.waitLoad(loadMeDiv)

    def login(self):
        loadMeDiv = '/html/body/div[1]/div/div/div/div/div/div[2]/div/form/input[4]'

        # Wait for page to fully load
        self.waitLoad(loadMeDiv)

        # login
        usernamePath = '/html/body/div[1]/div/div/div/div/div/div[2]/div/form/input[3]'
        passwordPath = '/html/body/div[1]/div/div/div/div/div/div[2]/div/form/input[4]'
        signInButton = '/html/body/div[1]/div/div/div/div/div/div[2]/div/form/button'

        self.driver.find_element_by_xpath(usernamePath).send_keys(self.user.userName)
        self.driver.find_element_by_xpath(passwordPath).send_keys(self.user.password)
        self.driver.find_element_by_xpath(signInButton).click()
        print("Logged In Successfully!")

    def waitLoad(self, pathToDiv, textOfDiv=None):
        stopBool = False
        while not stopBool:
            try:
                div = self.driver.find_element_by_xpath(pathToDiv)
                if textOfDiv == div.text or textOfDiv is None:
                    stopBool = True
            except NoSuchElementException:
                continue
        return






