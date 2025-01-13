# Stock Recommendation System

# Set up after clone repo
1. Create .env file in the root directory, with content (example for dev environment):

   ```env
   ### Airflow core settings
   AIRFLOW_IMAGE_NAME=apache/airflow:2.7.3
   AIRFLOW_UID=50000
   AIRFLOW_GID=1000
   _AIRFLOW_WWW_USER_USERNAME=airflow
   _AIRFLOW_WWW_USER_PASSWORD=airflow
   AIRFLOW_PROJ_DIR=.

   ### Environment-specific settings
   COMPOSE_PROJECT_NAME=airflow_dev
   POSTGRES_PORT=5433
   REDIS_PORT=6380
   WEBSERVER_PORT=8081
   FLOWER_PORT=5556
   POSTGRES_VOLUME_NAME=postgres-db-volume
   CONTAINER_PREFIX=dev
   ```
2. Initialize airflow database:
   ```bash
   docker-compose up airflow-init
   ```
3. Start all airflow services in detached mode with latest changes:
   ```bash
   docker-compose up -d --build
   ```
4. This container will own by airflow user, so you need to set the permissions to write in the directory :
   ```bash
   sudo chmod -R o+w dags/
   sudo chmod -R o+w logs/
   sudo chmod -R o+w plugins/
   sudo chmod -R o+w assets/
   ```
5. see running containers:
   ```bash
   docker ps
   ```
6. Stop all airflow services:
   ```bash
   docker-compose down
   ```


# Project Structure
## This project can run in two environments (prod and dev) simultaneously on the same machine:
- Prod: `/home/noam/projects/safeTrade/prod/backend_app/safeTrade_stocks_analysis_airflow_linux_os/`
- Dev: `/home/noam/projects/safeTrade/dev/backend_app/safeTrade_stocks_analysis_airflow_linux_os/`

## Environment Configuration
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

## Initialize the PostgreSQL database with the following commands:
CREATE DATABASE safe_trade;
CREATE USER airflow_user WITH PASSWORD 'airflow_usr123';
GRANT ALL PRIVILEGES ON DATABASE safe_trade TO airflow_user;


# More Commands
whoami  # Shows username
groups  # Shows groups

### take ownership of the directory - chown
sudo chown -R YOUR_USERNAME:YOUR_GROUP dags/
sudo chown -R YOUR_USERNAME:YOUR_GROUP logs/
sudo chown -R YOUR_USERNAME:YOUR_GROUP plugins/
sudo chown -R YOUR_USERNAME:YOUR_GROUP assets/

### Make directories writable by both you and Airflow
sudo chown -R noam:noam dags/
sudo chown -R noam:noam logs/
sudo chown -R noam:noam plugins/
sudo chown -R noam:noam assets/

### Set directory permissions
sudo chmod -R 775 dags/
sudo chmod -R 775 logs/
sudo chmod -R 775 plugins/
sudo chmod -R 775 assets/


### Troubleshooting - If you encounter permission issues, run:
docker exec -u root safetrade_stocks_analysis_airflow_linux_os-airflow-worker-1 chmod -R 777 /opt/airflow/assets
docker exec -u root safetrade_stocks_analysis_airflow_linux_os-airflow-webserver-1 chmod -R 777 /opt/airflow/assets
docker exec -u root safetrade_stocks_analysis_airflow_linux_os-airflow-scheduler-1 chmod -R 777 /opt/airflow/assets
docker exec -u root safetrade_stocks_analysis_airflow_linux_os-airflow-triggerer-1 chmod -R 777 /opt/airflow/assets