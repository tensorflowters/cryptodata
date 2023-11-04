# To launch a command line, type: make [target] [options].
# You need to have make installed on your system.
exportenv: var_docker_to_test_path=

devup:
	@echo "Starting project..."
	@docker compose up -d --build

devclean:
	@docker compose down --volumes --remove-orphans

initdb:
	@docker compose up airflow-init

airflow_info:
	@ ./airflow.sh info

airflow_migrate:
	@ ./airflow.sh db migrate

airflow_dag_list:
	@./airflow.sh dags list

airflow_dag_scrapin_cryptopanic_list:
	@./airflow.sh tasks list scrap_cryptopanic

airflow_dag_scrapin_cryptopanic_list_tree:
	@./airflow.sh tasks list scrap_cryptopanic --tree

# testing print_date
airflow_test_scrap_cryptopanic_print_date:
	@./airflow.sh tasks test scrap_cryptopanic print_date 2015-06-01

# testing sleep
airflow_test_scrap_cryptopanic_print_sleep:
	@./airflow.sh tasks test scrap_cryptopanic sleep 2015-06-01

# optional, start a web server in debug mode in the background
# airflow webserver --debug &

# start your backfill on a date range
airflow_backfill_scrap_cryptopanic:
	@./airflow dags backfill scrap_cryptopanic \
    	--start-date 2015-06-01 \
    	--end-date 2015-06-07