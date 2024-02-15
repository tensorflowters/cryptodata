ENV?=env-vars/.env.ansible.prod

include $(ENV)
export $(shell sed 's/=.*//' $(ENV))

DOCKER_CMD=docker compose -p cryptodata_deployment -f docker/docker-compose-ansible.prod.yml --env-file $(ENV)

prod_run:
	@${DOCKER_CMD} up -d --build