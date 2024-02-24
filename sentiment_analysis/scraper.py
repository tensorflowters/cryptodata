from driver import FirefoxDriver # type: ignore
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def get_binance_article_content(uri: str) -> str:
    driver = FirefoxDriver()
    driver.get(uri)
    WebDriverWait(driver.driver, 10).until(
        EC.presence_of_element_located((By.ID, "articleBody"))
    )

    container = driver.find_element_by_xpath("//*[@id='articleBody']/div")
    paragraphs = driver.find_multiple_elements_by_class_name(container, "richtext-paragraph")
    text = ""
    for paragraph in paragraphs:
        text += paragraph.text

    return text