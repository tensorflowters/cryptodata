# Communicate on changes make to the codebase here

## Arthur - 20/10/2023 - Creating a test scrapper for new app architecture

### Description

I just a make a scraper that sending back data to test the new architecture of the app.
We'll keep same arch as v2 but with a spark job between kafka and the database where to save data.
New workflow:

- Airflow run a scrapping job every x minutes
- Airflow result is sending to kafka
- Kafka send data to spark
- Spark format data
- Spark save data to database
- Grafana display data from database (not yet added to compose file)

README.md is probably not up to date, I'll update it later.
