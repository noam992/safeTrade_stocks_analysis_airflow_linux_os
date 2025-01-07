# Stock Recommendation System

## Initial Setup

# Add your user to Docker group and apply changes
sudo usermod -aG docker $USER
newgrp docker

# Verify Docker setup
docker --version
docker ps


## Docker Commands

# Build and start containers
docker-compose up -d --build

# Check container status
docker ps

# View logs
docker logs safetrade_stocks_analysis_airflow_linux_os-airflow-worker-1

# Stop containers
docker-compose down


## Troubleshooting - If you encounter permission issues, run:
docker exec -u root safetrade_stocks_analysis_airflow_linux_os-airflow-worker-1 chmod -R 777 /opt/airflow/assets
docker exec -u root safetrade_stocks_analysis_airflow_linux_os-airflow-webserver-1 chmod -R 777 /opt/airflow/assets
docker exec -u root safetrade_stocks_analysis_airflow_linux_os-airflow-scheduler-1 chmod -R 777 /opt/airflow/assets
docker exec -u root safetrade_stocks_analysis_airflow_linux_os-airflow-triggerer-1 chmod -R 777 /opt/airflow/assets
