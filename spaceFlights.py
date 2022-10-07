from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class SpaceFlights:

    def __init__(self, url, xpath):
        self.url = url
        self.xpath = xpath

    def get_new_url(self):
        # Here Chrome  will be used
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        # URL of website
        url = self.url
        # Opening the website
        driver.get(url)
        # Getting the button by element xpath
        button = driver.find_element(By.XPATH, self.xpath)
        # Clicking on the button
        button.click()
        # Getting new url
        new_url = driver.current_url

        return new_url
