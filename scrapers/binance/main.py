import hashlib
import json
import os

import pendulum
from kafka import KafkaProducer
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager


def get_sha256_hash(url):
    m = hashlib.sha256()
    m.update(url.encode("utf-8"))
    return m.hexdigest()


TARGET = "https://www.binance.com/en/feed"
gecko_driver = GeckoDriverManager().install()

# Initialize Firefox options
options = webdriver.FirefoxOptions()

# Run in headless mode
options.add_argument("-headless")

# Initialize the Firefox WebDriver with the options
driver = webdriver.Firefox(options=options, service=Service(gecko_driver))

# Navigate to a webpage
driver.get(TARGET)

try:
    # Waiting 10 seconds for the element to be located
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "FeedList"))
    )

    target_main_section = driver.find_element(
        By.XPATH, "//*[@id='feed-home-tabs']/div[2]/div[3]"
    )

    # Select all the news cards
    target_news_cards = target_main_section.find_elements(By.CLASS_NAME, "feed-card")

    producer = KafkaProducer(
        bootstrap_servers=[os.environ.get("KAFKA_BROKER")],
        value_serializer=lambda m: json.dumps(m).encode("ascii"),
    )

    # Loop through the news cards
    for news_card in target_news_cards:
        # Required informations
        currencies = []
        hashed_url = None
        link_page = None
        published_at = None
        published_at_timestamp = None
        publish_from_when_scraped = None
        source_domain = None
        title = None

        # Extract the time from wich the news was published
        publised_from_element = news_card.find_element(
            By.CSS_SELECTOR,
            ".card__hd .create-time",
        )
        if publised_from_element is not None and publised_from_element.text != "":
            publish_from_when_scraped = publised_from_element.text

            # Calculate the published time from the published from extracted time
            if "min" in publish_from_when_scraped or "h" in publish_from_when_scraped:
                tz = pendulum.timezone("UTC")
                now = pendulum.now(tz=tz)
                if "min" not in publish_from_when_scraped:
                    dt = now.subtract(
                        hours=int(publish_from_when_scraped.split("h")[0])
                    )
                    if dt is not None:
                        published_at = dt.to_rfc850_string()
                        published_at_timestamp = int(dt.timestamp() * 1000)
                elif "min" in publish_from_when_scraped:
                    dt = now.subtract(
                        minutes=int(publish_from_when_scraped.split("m")[0])
                    )
                    if dt is not None:
                        published_at = dt.to_rfc850_string()
                        published_at_timestamp = int(dt.timestamp() * 1000)

        # Extract the source domain of the news
        source_domain_element = news_card.find_element(
            By.CSS_SELECTOR,
            ".avatar-nick-container .nick-username .nick",
        )

        if source_domain_element is not None and source_domain_element.text != "":
            source_domain = source_domain_element.text

        # Extract the title of the news
        try:
            title_element = news_card.find_element(By.CSS_SELECTOR, ".card__title h3")
            if title_element is not None and title_element.text != "":
                title = title_element.text
        except NoSuchElementException:
            pass

        # Extract the currencies of the news. Possible to have multiple currencies or none
        trading_pairs = news_card.find_elements(By.CSS_SELECTOR, ".trading-pairs")
        if trading_pairs:
            if len(trading_pairs) > 0:
                for currency in trading_pairs:
                    currency_text = currency.find_element(By.CSS_SELECTOR, ".symbol")
                    if (
                        currency_text is not None
                        and currency_text.text != ""
                        and currency_text.text not in currencies
                    ):
                        currencies.append(currency_text.text)

        # Extract the link of the news on the scrapped website
        link_page_element = news_card.find_element(
            By.CSS_SELECTOR, ".feed-content-text > a"
        ).get_attribute("href")
        if link_page_element is not None and link_page_element != "":
            link_page = link_page_element
            hashed_url = get_sha256_hash(link_page)

        # Check if the required informations are not empty
        # Need to check here if hashed_url already exists in the database
        if hashed_url is not None or hashed_url != "":
            # Create the news object (dictionary)
            scraped_news = {
                "currencies": currencies,
                "hashed_url": hashed_url,
                "link_page": link_page,
                "published_at": published_at,
                "published_at_timestamp": published_at_timestamp,
                "publish_from_when_scraped": publish_from_when_scraped,
                "source_domain": source_domain,
                "title": title,
            }
            producer.send("scraped_news", scraped_news)
            producer.flush()
            # Convert the news object to json
            scraped_news_to_json = json.dumps(scraped_news)

            # Output the news object
            print(scraped_news_to_json)

        else:
            print("Invalid scraped data")
finally:
    # else quit
    driver.quit()
