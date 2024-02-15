# To launch a command line, type: make [target] [options].
# You need to have make installed on your system.

MAKE_EXECUTOR_ENV=make -f commands/dev.mk
MAKE_EXECUTOR_REGISTERY=make -f commands/docker-build.mk
MAKE_EXECUTOR_DEPLOY=make -f commands/deploy.mk

devup:
	@${MAKE_EXECUTOR_ENV} devup

devuprm:
	@${MAKE_EXECUTOR_ENV} devuprm

devclean:
	@${MAKE_EXECUTOR_ENV} devclean

build_registery_all:
	@${MAKE_EXECUTOR_REGISTERY} build_cryptodata-cryptopanic-scraper
	@${MAKE_EXECUTOR_REGISTERY} build_cryptodata-binance-scraper
	@${MAKE_EXECUTOR_REGISTERY} build_cryptodata-airflow
	@${MAKE_EXECUTOR_REGISTERY} build_cryptodata-scraped_consumer
	@${MAKE_EXECUTOR_REGISTERY} build_cryptodata-wss
	@${MAKE_EXECUTOR_REGISTERY} build_cryptodata-spark
	@${MAKE_EXECUTOR_REGISTERY} build_cryptodata-client_initdb


prod_run:
	@${MAKE_EXECUTOR_DEPLOY} prod_run

prod_apply_deployment:
	@microk8s kubectl apply -f deployment/k8s/configmaps
	@microk8s kubectl apply -f deployment/k8s/pvcs
	@microk8s kubectl apply -f deployment/k8s/jobs
	@microk8s kubectl apply -f deployment/k8s/deployments
	@microk8s kubectl apply -f deployment/k8s/services
	@microk8s kubectl apply -f deployment/k8s/ingress