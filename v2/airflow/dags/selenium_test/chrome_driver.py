from selenium import webdriver
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()

driver = webdriver.Remote(
    command_executor='http://chrome:4444',
    options=chrome_options
)

driver.get("https://cryptopanic.com")

title = driver.title

print(title)

driver.implicitly_wait(2)

test = driver.find_element(By.ID, "menuToggle")

print(test)

driver.quit()