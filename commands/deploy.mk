ENV?=env-vars/.env.ansible.prod

include $(ENV)
export $(shell sed 's/=.*//' $(ENV))

DOCKER_CMD=docker compose -p cryptodata_deployment -f docker/docker-compose-ansible.prod.yml --env-file $(ENV)

gen_ssh_key:
	@/bin/bash -c "ssh-keygen -q -t ed25519 -N '${SERVER_03100_USER_SSH_PASS}' -f deployment/ansible/.ssh_config/${SERVER_03100_SSH_KEY_NAME} <<<y >/dev/null 2>&1"
	@chown -R 1000:1000 deployment/ansible/.ssh_config
	@chmod 600 deployment/ansible/.ssh_config/${SERVER_03100_SSH_KEY_NAME}

deploy:
	@${DOCKER_CMD} up -d --build