from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize Firefox options
options = webdriver.FirefoxOptions()

# Run in headless mode
options.add_argument("-headless")
# firefox_options.executable_path = '/usr/local/bin/geckodriver'
# firefox_options.binary_location = '/usr/bin/firefox'
# firefox_options.log.level = 'trace'


# Initialize the Firefox WebDriver with the options
driver = webdriver.Firefox(options=options)

# Navigate to a webpage
driver.get('https://cryptopanic.com')

try:
    # wait 10 seconds before looking for element
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "news"))
    )
    # Perform any interactions
    print(driver.title)
    news = driver.find_elements(By.CLASS_NAME, "news-row")
    print(news)
finally:
    # else quit
    driver.quit()