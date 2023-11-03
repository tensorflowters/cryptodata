# Communicate on changes make to the codebase here

## Arthur - 20/10/2023 - Creating a test scrapper for new app architecture

### Description - Creating a test scrapper for new app architecture

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

### Update

Finished a working testing scraper

## Arthur - 21/10/2023 - Integrating Apache airflow

### Description - Integrating Apache airflow

I initialized tha airflow stack and learned how to use it very basically.
I don't have found a answer yet but I'm asking if the scripts or services to execute should be created and managed in the airflow stack (like the demo seem to indicate) or
if we should keep our services isolated from the airflow stack and just use airflow to run them.
If it's the second option, I'll have to find a way to manage the services from the airflow stack.
I hadn't found yep a way to do it. Please don't hesitate to give me your opinion on this.
