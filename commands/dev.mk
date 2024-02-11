include env-vars/.env.dev
export $(shell sed 's/=.*//' env-vars/.env.dev)

AIRFLOW_EXECUTOR=airflow/airflow.sh
DOCKER_EXECUTOR=docker compose -f docker/docker-compose.dev.yml -p cryptodata

devup:
	@${DOCKER_EXECUTOR} up -d --build

devuprm:
	@${DOCKER_EXECUTOR} up -d --build
	@${DOCKER_EXECUTOR} rm --force airflow-init
	@${DOCKER_EXECUTOR} rm --force client_initdb

devclean:
	@${DOCKER_EXECUTOR} down --volumes --remove-orphans --rmi local

initdb:
	@${DOCKER_EXECUTOR} up airflow-init

airflow_info:
	@${AIRFLOW_EXECUTOR} info

airflow_migrate:
	@${AIRFLOW_EXECUTOR} db migrate

airflow_dag_list:
	@${AIRFLOW_EXECUTOR} dags list

airflow_dag_scrapin_cryptopanic_list:
	@${AIRFLOW_EXECUTOR} tasks list scrap_cryptopanic

airflow_dag_scrapin_cryptopanic_list_tree:
	@${AIRFLOW_EXECUTOR} tasks list scrap_cryptopanic --tree

# testing print_date
airflow_test_scrap_cryptopanic_print_date:
	@${AIRFLOW_EXECUTOR} tasks test scrap_cryptopanic print_date 2015-06-01

# testing sleep
airflow_test_scrap_cryptopanic_print_sleep:
	@${AIRFLOW_EXECUTOR} tasks test scrap_cryptopanic sleep 2015-06-01

# optional, start a web server in debug mode in the background
# airflow webserver --debug &

# start your backfill on a date range
airflow_backfill_scrap_cryptopanic:
	@${AIRFLOW_EXECUTOR} dags backfill scrap_cryptopanic \
    	--start-date 2015-06-01 \
    	--end-date 2015-06-07