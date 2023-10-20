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
    # print(driver.title)
    news_rows = driver.find_elements(By.CLASS_NAME, "news-row")

    for news_row in news_rows:
        # Extract required information
        time_element = news_row.find_element(By.XPATH, "//div[@class='news-cells']")
        time_url = time_element.find_element(By.CLASS_NAME, "nc-date")
        time_container = time_url.find_element(By.TAG_NAME, "span")
        time_tag_element = time_container.find_element(By.XPATH, "//time")
        time = time_tag_element.get_attribute('datetime')

        # title_element = news_row.find_element(By.CSS_SELECTOR, '.news-cell.nc-title span.title-text span')
        # title = title_element.text

        # source_element = news_row.find_element(By.CSS_SELECTOR, '.si-source-domain')
        # source = source_element.text

        # currency_elements = news_row.find_elements(By.CSS_SELECTOR, '.news-cell.nc-currency .colored-link')
        # currencies = [el.text for el in currency_elements]

        #Create the news object (dictionary)
        news_object = {
            'Time': time,
            # 'Title': title,
            # 'Source': source,
            # 'Currencies': currencies
        }

        # Output the news object
        print(news_object)
finally:
    # else quit
    driver.quit()