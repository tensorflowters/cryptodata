# To launch a command line, type: make [target] [options].
# You need to have make installed on your system.

MAKE_EXECUTOR_DEV=make -f commands/dev.mk
MAKE_EXECUTOR_DEPLOY=make -f commands/prod.mk
MAKE_EXECUTOR_REGISTERY=make -f commands/docker-build.mk


devup:
	@${MAKE_EXECUTOR_DEV} devup

devuprm:
	@${MAKE_EXECUTOR_DEV} devuprm

devclean:
	@${MAKE_EXECUTOR_DEV} devclean

fix_grafana_permissions:
	@${MAKE_EXECUTOR_DEV} fix_grafana_permissions


prod_stop:
	@${MAKE_EXECUTOR_DEPLOY} prod_stop

prod_build:
	@${MAKE_EXECUTOR_DEPLOY} prod_build

prod_up:
	@${MAKE_EXECUTOR_DEPLOY} prod_up

prod_clean:
	@${MAKE_EXECUTOR_DEPLOY} prod_rm


build_registery_all:
	@${MAKE_EXECUTOR_REGISTERY} build_cryptodata-airflow
	@${MAKE_EXECUTOR_REGISTERY} build_cryptodata-binance-scraper
	@${MAKE_EXECUTOR_REGISTERY} build_cryptodata-client_initdb
	@${MAKE_EXECUTOR_REGISTERY} build_cryptodata-cryptopanic-scraper
	@${MAKE_EXECUTOR_REGISTERY} build_cryptodata-scraped_consumer
	@${MAKE_EXECUTOR_REGISTERY} build_cryptodata-sentiment_analysis
	@${MAKE_EXECUTOR_REGISTERY} build_cryptodata-wss