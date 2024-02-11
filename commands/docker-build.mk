include env-vars/.env.dockerhub
export $(shell sed 's/=.*//' env-vars/.env.dockerhub)

build_img: img=default
build_img: tag=latest
build_img:
	@docker build -t ${DOCKERHUB_LOGIN}/${img}:${tag} .
	@docker login -p ${DOCKERHUB_PASSWD} -u ${DOCKERHUB_LOGIN}
	@docker push ${DOCKERHUB_LOGIN}/cryptodata:${img}:${tag}

build_cryptodata-spark:
	@docker build -f $(PWD)/spark/spark.dockerfile -t ${DOCKERHUB_LOGIN}/cryptodata:cryptodata-spark .
	@docker login -p ${DOCKERHUB_PASSWD} -u ${DOCKERHUB_LOGIN}
	@docker push ${DOCKERHUB_LOGIN}/cryptodata:cryptodata-spark
build_cryptodata-wss:
	@docker build -f $(PWD)/crypto-wss/wss.dockerfile -t ${DOCKERHUB_LOGIN}/cryptodata:cryptodata-wss .
	@docker login -p ${DOCKERHUB_PASSWD} -u ${DOCKERHUB_LOGIN}
	@docker push ${DOCKERHUB_LOGIN}/cryptodata:cryptodata-wss
build_cryptodata-scraped_consumer:
	@docker build -f $(PWD)/consumers/scraped/scraped.dockerfile -t ${DOCKERHUB_LOGIN}/cryptodata:cryptodata-scraped_consumer .
	@docker login -p ${DOCKERHUB_PASSWD} -u ${DOCKERHUB_LOGIN}
	@docker push ${DOCKERHUB_LOGIN}/cryptodata:cryptodata-scraped_consumer
build_cryptodata-airflow:
	@docker build -f $(PWD)/airflow/airflow.dockerfile -t ${DOCKERHUB_LOGIN}/cryptodata:cryptodata-airflow .
	@docker login -p ${DOCKERHUB_PASSWD} -u ${DOCKERHUB_LOGIN}
	@docker push ${DOCKERHUB_LOGIN}/cryptodata:cryptodata-airflow
build_cryptodata-binance-scraper:
	@docker build -f $(PWD)/scrapers/binance/scraper.dockerfile -t ${DOCKERHUB_LOGIN}/cryptodata:cryptodata-binance-scraper .
	@docker login -p ${DOCKERHUB_PASSWD} -u ${DOCKERHUB_LOGIN}
	@docker push ${DOCKERHUB_LOGIN}/cryptodata:cryptodata-binance-scraper
build_cryptodata-cryptopanic-scraper:
	@docker build -f $(PWD)/scrapers/cryptopanic/scraper.dockerfile -t ${DOCKERHUB_LOGIN}/cryptodata:cryptodata-cryptopanic-scraper .
	@docker login -p ${DOCKERHUB_PASSWD} -u ${DOCKERHUB_LOGIN}
	@docker push ${DOCKERHUB_LOGIN}/cryptodata:cryptodata-cryptopanic-scraper
build_cryptodata-client_initdb:
	@docker build -f $(PWD)/db/initdb.dockerfile -t ${DOCKERHUB_LOGIN}/cryptodata:cryptodata-client_initdb .
	@docker login -p ${DOCKERHUB_PASSWD} -u ${DOCKERHUB_LOGIN}
	@docker push ${DOCKERHUB_LOGIN}/cryptodata:cryptodata-client_initdb