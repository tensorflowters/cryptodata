DOCKER_EXECUTOR=docker compose -f docker/docker-compose.prod.yml -p cryptodata --env-file ./.env

prod_stop:
	@${DOCKER_EXECUTOR} stop

prod_build:
	@${DOCKER_EXECUTOR} build --no-cache

prod_up:
	@${DOCKER_EXECUTOR} up -d

prod_rm:
	@docker container prune -f
	@docker image prune -f