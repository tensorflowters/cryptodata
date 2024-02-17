DOCKER_EXECUTOR=docker compose -f docker/docker-compose.prod.yml -p cryptodata

prod_stop:
	@${DOCKER_EXECUTOR} stop

prod_build:
	@${DOCKER_EXECUTOR} --env-file .env build --no-cache

prod_up:
	@${DOCKER_EXECUTOR} --env-file .env up -d

prod_rm:
	@docker container prune -f
	@docker image prune -f