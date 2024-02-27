include env-vars/.env.dockerhub
export $(shell sed 's/=.*//' env-vars/.env.dockerhub)

build_img: img=default
build_img: tag=latest
build_img:
	@docker build -t ${DOCKER_HUB_USERNAME}/${img}:${tag} .
	@docker login -p ${DOCKER_HUB_PASSWORD} -u ${DOCKER_HUB_USERNAME}
	@docker push ${DOCKER_HUB_USERNAME}/cryptodata:${img}:${tag}

build_cryptodata-wss:
	@docker build -f $(PWD)/crypto-wss/wss.dockerfile -t ${DOCKER_HUB_USERNAME}/cryptodata:cryptodata-wss .
	@docker login -p ${DOCKER_HUB_PASSWORD} -u ${DOCKER_HUB_USERNAME}
	@docker push ${DOCKER_HUB_USERNAME}/cryptodata:cryptodata-wss
build_cryptodata-scraped_consumer:
	@docker build -f $(PWD)/consumers/scraped/scraped.dockerfile -t ${DOCKER_HUB_USERNAME}/cryptodata:cryptodata-scraped_consumer .
	@docker login -p ${DOCKER_HUB_PASSWORD} -u ${DOCKER_HUB_USERNAME}
	@docker push ${DOCKER_HUB_USERNAME}/cryptodata:cryptodata-scraped_consumer
build_cryptodata-airflow:
	@docker build -f $(PWD)/airflow/airflow.dockerfile -t ${DOCKER_HUB_USERNAME}/cryptodata:cryptodata-airflow .
	@docker login -p ${DOCKER_HUB_PASSWORD} -u ${DOCKER_HUB_USERNAME}
	@docker push ${DOCKER_HUB_USERNAME}/cryptodata:cryptodata-airflow
build_cryptodata-binance-scraper:
	@docker build -f $(PWD)/scrapers/binance/scraper.dockerfile -t ${DOCKER_HUB_USERNAME}/cryptodata:cryptodata-binance-scraper .
	@docker login -p ${DOCKER_HUB_PASSWORD} -u ${DOCKER_HUB_USERNAME}
	@docker push ${DOCKER_HUB_USERNAME}/cryptodata:cryptodata-binance-scraper
build_cryptodata-cryptopanic-scraper:
	@docker build -f $(PWD)/scrapers/cryptopanic/scraper.dockerfile -t ${DOCKER_HUB_USERNAME}/cryptodata:cryptodata-cryptopanic-scraper .
	@docker login -p ${DOCKER_HUB_PASSWORD} -u ${DOCKER_HUB_USERNAME}
	@docker push ${DOCKER_HUB_USERNAME}/cryptodata:cryptodata-cryptopanic-scraper
build_cryptodata-client_initdb:
	@docker build -f $(PWD)/db/initdb.dockerfile -t ${DOCKER_HUB_USERNAME}/cryptodata:cryptodata-client_initdb .
	@docker login -p ${DOCKER_HUB_PASSWORD} -u ${DOCKER_HUB_USERNAME}
	@docker push ${DOCKER_HUB_USERNAME}/cryptodata:cryptodata-client_initdb

build_cryptodata-sentiment_analysis:
	@docker build -f $(PWD)/sentiment_analysis/sa.dockerfile -t ${DOCKER_HUB_USERNAME}/cryptodata:cryptodata-sentiment_analysis .
	@docker login -p ${DOCKER_HUB_PASSWORD} -u ${DOCKER_HUB_USERNAME}
	@docker push ${DOCKER_HUB_USERNAME}/cryptodata:cryptodata-sentiment_analysis