include env-vars/.env.prod
export $(shell sed 's/=.*//' env-vars/.env.prod)

print_ansible_home:
	@echo ${ANSIBLE_HOME}

check_host_python:
	@cd ./ansible && poetry run ansible -m command -a "python -V" k8s_cluster_01