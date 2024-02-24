# Cryptodata

## Notes

### Scraping

- You need to pass in a `GH_TOKEN` env value (A github token) to be able to scrap websites

### Live data

To run the WSS script and feed live data to the database:

- You need to create a [blockchain account](https://www.exchange.blockchain.com) and get an api key
- You need to pass in a `BLOCKCHAIN_API_KEY` env value
- You need to then run `./run.sh wss` to start the websocket script

## Sytem Design

### Web scrapper

The following tools will be use to scrap the data from the news feed:

- [Scrapy](https://scrapy.org/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

These are robust and widely used for web scraping.

### Data Storage

Depending on the volume and nature of our data, we should consider using a combination of relational databases (like PostgreSQL) and NoSQL databases (like MongoDB or Elasticsearch)

- [PostgreSQL](https://www.postgresql.org/)
- [MongoDB](https://www.mongodb.com/)
- [Elasticsearch](https://www.elastic.co/)
- [InfluxDB](https://www.influxdata.com/)
- [TimescaleDB](https://www.timescale.com/)

### Data Builder (Processing)

The following tools will be use to real-time data processing, especially if wz expect high volumes of data.

- [Apache Kafka](https://kafka.apache.org/)

It can also handle batch processing, so it offers flexibility.

Apache Kafka can be used in conjunction with pytorch to handle real-time data ingestion and processing.
Kafka can act as a buffer to store the scraped data.
Depending on the kind of analytics we're running, a time-series database like InfluxDB or TimescaleDB might be beneficial.

### Monitoring & Error Handling

Since we're setting up a pipeline, we should have monitoring and alerting in place. Tools like Prometheus and Alertmanager can be integrated with Grafana to provide monitoring capabilities.

- [Prometheus](https://prometheus.io/)
- [Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/)

### Dynamic Viewer with Analytics

The following tools will be use to visualize the data:

- [Grafana](https://grafana.com/)

Grafana is a solid choice for visualizing time-series data. It integrates well with many databases, including InfluxDB and TimescaleDB.

We should ensure we have the right plugins or visualizations to represent the analytics as you envision.

Grafana has a rich library of plugins.

For more interactive and custom analytics visualization, we could consider using Tableau or Power BI.

### Infrastructure

We'll use a self-managed system and maybe Kubernetes to manage the infrastructure.

- [Kubernetes](https://kubernetes.io/)
- [Docker](https://www.docker.com/)

### Automation

We should also consider setting up an automation tool or CI/CD pipeline, like Jenkins or GitHub Actions, to deploy updates and changes to our system seamlessly.

- [Jenkins](https://www.jenkins.io/)
- [GitHub Actions](https://github.com)

## Feeds

We'll use the following news feeds:

- [CryptoPanic](https://cryptopanic.com/news/)

## Data schema

## News object

A news should have the following attributes:

- `id`: unique identifier
- `title`: title of the news
- `datetime`: date of the news
- `description`: description of the news
- `url`: url of the news
