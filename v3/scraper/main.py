from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pendulum
import hashlib
import json

def get_sha256_hash(url):
    m = hashlib.sha256()
    m.update(url.encode('utf-8'))
    return m.hexdigest()

TARGET="https://cryptopanic.com"

# Initialize Firefox options
options = webdriver.FirefoxOptions()

# Run in headless mode
options.add_argument("-headless")

# Initialize the Firefox WebDriver with the options
driver = webdriver.Firefox(options=options)

# Navigate to a webpage
driver.get(TARGET)

try:
    # Waiting 10 seconds for the element to be located
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "news"))
    )

    # Select the main app news section
    target_main_section = driver.find_element(By.XPATH, ".//div[@class='app-main-pane']")

    # Select all the news rows
    target_news_rows = target_main_section.find_elements(By.CLASS_NAME, "news-row")

    # Loop through the news rows
    for news_row in target_news_rows:
        # Required informations
        currencies = []
        hashed_url = None
        link_page = None
        published_at = None
        publish_from_when_scraped = None
        source_domain = None
        title = None

        # Extract the time from wich the news was published
        publised_from_element = news_row.find_element(
            By.XPATH, ".//div[@class='news-cells']//a[@class='news-cell nc-date']"
        )
        if publised_from_element is not None and publised_from_element.text != '':
            publish_from_when_scraped = publised_from_element.text

            # Calculate the published time from the published from extracted time
            if 'min' in publish_from_when_scraped or 'h' in publish_from_when_scraped:
                tz = pendulum.timezone('UTC')
                now = pendulum.now(tz=tz)
                if 'min' not in publish_from_when_scraped:
                    dt = now.subtract(hours=int(publish_from_when_scraped.split('h')[0]))
                    if dt is not None:
                        published_at = dt.to_rfc850_string()
                elif 'min' in publish_from_when_scraped:
                    dt = now.subtract(minutes=int(publish_from_when_scraped.split('m')[0]))
                    if dt is not None:
                        published_at = dt.to_rfc850_string()

        # Extract the source domain of the news
        source_domain_element = news_row.find_element(
            By.XPATH, ".//div[@class='news-cells']//a[@class='news-cell nc-title']//span[@class='si-source-name']//span[@class='si-source-domain']"
        )
        if source_domain_element is not None and source_domain_element.text != '':
            source_domain = source_domain_element.text

        # Extract the title of the news
        title_element = news_row.find_element(
            By.XPATH, ".//div[@class='news-cells']//a[@class='news-cell nc-title']"
        )
        if title_element is not None and title_element.text != '':
            title = title_element.text
            if source_domain != None and source_domain != '' and source_domain in title:
                title = title.replace(source_domain, '')

        # Extract the currencies of the news. Possible to have multiple currencies or none
        if news_row.find_elements(By.XPATH, ".//div[@class='news-cells']//div[@class='news-cell nc-currency']"):
            currencies_element = news_row.find_elements(
                By.XPATH, ".//div[@class='news-cells']//div[@class='news-cell nc-currency']//a"
            )
            if len(currencies_element) > 0:
                for currency in currencies_element:
                    if currency != None and currency.text != '' and currency.text not in currencies:
                        currencies.append(currency.text)

        # Extract the link of the news on the scrapped website
        link_page_element = news_row.find_element(
            By.XPATH, ".//a[@class='click-area']"
        ).get_attribute('href')
        if link_page_element is not None and link_page_element != '':
            link_page = link_page_element
            hashed_url = get_sha256_hash(link_page)

        # Check if the required informations are not empty
        # Need to check here if hashed_url already exists in the database
        if hashed_url != None or hashed_url != '':
            # Create the news object (dictionary)
            scraped_news = {
                "currencies": currencies,
                "hashed_url": hashed_url,
                "link_page": link_page,
                "published_at": published_at,
                "publish_from_when_scraped": publish_from_when_scraped,
                "source_domain": source_domain,
                "title": title
            }

            # Convert the news object to json
            scraped_news_to_json = json.dumps(scraped_news)

            # Output the news object
            print(scraped_news_to_json)
        else:
            print("Invalid scraped data")
finally:
    # else quit
    driver.quit()
