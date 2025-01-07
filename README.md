# Stock Recommendation System

## Project Structure
This project can run in two environments (prod and dev) simultaneously on the same machine:
- Prod: `/home/noam/projects/safeTrade/prod/backend_app/safeTrade_stocks_analysis_airflow_linux_os/`
- Dev: `/home/noam/projects/safeTrade/dev/backend_app/safeTrade_stocks_analysis_airflow_linux_os/`

## Initial Setup

### Docker Setup

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

### Environment Configuration
Each environment uses its own `.env` file with different ports and names:
- Prod Environment:
  - Webserver: http://localhost:8080
  - Postgres: 5432
  - Redis: 6379
  - Flower: 5555

- Dev Environment:
  - Webserver: http://localhost:8081
  - Postgres: 5433
  - Redis: 6380
  - Flower: 5556

## Docker Commands

### Production Environment

# List all volumes
docker volume ls

# Remove specific volume
docker volume rm [volume_name]