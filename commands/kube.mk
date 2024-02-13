k8s_dashboard:
	@microk8s dashboard-proxy

k8s_services:
	@microk8s kubectl get services

k8s_help:
	@microk8s kubectl --help

k8s_apply_airflow:
	@kubectl apply -f airflow-config-pvc.yml
	@kubectl apply -f airflow-init-script-configmap.yml
	@kubectl apply -f airflow-configmap.yml
	@kubectl apply -f airflow-dags-pvc.yml
	@kubectl apply -f airflow-logs-pvc.yml
	@kubectl apply -f airflow-plugins-pvc.yml
	@kubectl apply -f airflow-secrets.yml
	@kubectl apply -f airflow-worker-deployment.yml
	@kubectl apply -f airflow-scheduler-deployment.yml
	@kubectl apply -f airflow-triggerer-deployment.yml
	@kubectl apply -f airflow-webserver-deployment.yml
	@kubectl apply -f airflow-webserver-service.yml
	@kubectl apply -f airflow-webserver-ingress.yml
	@kubectl apply -f airflow-cli-job.yml

k8s_apply_airflow_db:
	@kubectl apply -f airflow-db-secrets.yml
	@kubectl apply -f airflow-db-pvc.yml
	@kubectl apply -f airflow-db-deployment.yml
	@kubectl apply -f airflow-db-service.yml

k8s_apply_client_db:
	@kubectl apply -f client-db-secrets.yml
	@kubectl apply -f client-db-pvc.yml
	@kubectl apply -f client-db-deployment.yml
	@kubectl apply -f client-db-service.yml
	@kubectl apply -f client-db-init-job.yml

k8s_apply_redis:
	@kubectl apply -f redis-deployment.yml
	@kubectl apply -f redis-service.yml
	@kubectl apply -f redis-pvc.yml
	@kubectl apply -f redis-secrets.yml

k8s_apply_zookeeper:
	@kubectl apply -f zookeeper-configmap.yml
	@kubectl apply -f zookeeper-pvc.yml
	@kubectl apply -f zookeeper-deployment.yml
	@kubectl apply -f zookeeper-service.yml

k8s_apply_kafka:
	@kubectl apply -f kafka-configmap.yml
	@kubectl apply -f kafka-deployment.yml
	@kubectl apply -f kafka-service.yml