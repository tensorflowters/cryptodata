from typing import List
from threading import Lock
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    """

    _instances = {} # type: ignore

    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class FirefoxDriver(metaclass=SingletonMeta):
    driver: WebDriver

    def __init__(self):
        gecko_driver = GeckoDriverManager().install()

        options = webdriver.FirefoxOptions()

        options.add_argument("-headless")

        self.driver = webdriver.Firefox(options=options, service=Service(gecko_driver))

    def get(self, url) -> None:
        self.driver.get(url)

    def find_element_by_xpath(self, xpath: str) -> WebElement:
        return self.driver.find_element(By.XPATH, xpath)

    def find_multiple_elements_by_class_name(self, parent_el: WebElement, class_name: str) -> List[WebElement]:
        return parent_el.find_elements(By.CLASS_NAME, class_name)

    def close(self) -> None:
        self.driver.close()