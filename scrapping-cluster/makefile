include ./.env
export $(shell sed 's/=.*//' ./.env)

devup:
	@docker compose --env-file ./.env up -d --build

test:
	@docker compose --env-file ./.env exec kafka_monitor /bin/sh /usr/src/app/run_docker_tests.sh
	@docker compose --env-file ./.env exec redis_monitor /bin/sh /usr/src/app/run_docker_tests.sh
	@docker compose --env-file ./.env exec rest /bin/sh /usr/src/app/run_docker_tests.sh
	@docker compose --env-file ./.env exec crawler /bin/sh /usr/src/app/run_docker_tests.sh
