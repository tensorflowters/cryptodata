k8s_dashboard:
	@microk8s dashboard-proxy

k8s_services:
	@microk8s kubectl get services

k8s_help:
	@microk8s kubectl --help

k8s_apply_airflow_webserver:
	@kubectl apply -f airflow-config-pvc.yml
	@kubectl apply -f airflow-configmap.yml
	@kubectl apply -f airflow-dags-pvc.yml
	@kubectl apply -f airflow-logs-pvc.yml
	@kubectl apply -f airflow-plugins-pvc.yml
	@kubectl apply -f airflow-secrets.yml
	@kubectl apply -f airflow-webserver-deployment.yml
	@kubectl apply -f airflow-webserver-service.yml
	@kubectl apply -f airflow-webserver-ingress.yml