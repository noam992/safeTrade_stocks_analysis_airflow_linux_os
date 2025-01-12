# Stock Recommendation System

## Project Structure
This project can run in two environments (prod and dev) simultaneously on the same machine:
- Prod: `/home/noam/projects/safeTrade/prod/backend_app/safeTrade_stocks_analysis_airflow_linux_os/`
- Dev: `/home/noam/projects/safeTrade/dev/backend_app/safeTrade_stocks_analysis_airflow_linux_os/`


## Docker Commands
### To chack if any docker is running:
docker ps

### To set the airflow running user:
docker-compose up -d --build

### Stop containers
docker-compose down


## Permissions Commands
### if you want to modify files in the airflow directory, you need to run the command
### then the permissions of airflow user will removed
whoami  # Shows username
groups  # Shows groups

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


## Troubleshooting - If you encounter permission issues, run:
docker exec -u root safetrade_stocks_analysis_airflow_linux_os-airflow-worker-1 chmod -R 777 /opt/airflow/assets
docker exec -u root safetrade_stocks_analysis_airflow_linux_os-airflow-webserver-1 chmod -R 777 /opt/airflow/assets
docker exec -u root safetrade_stocks_analysis_airflow_linux_os-airflow-scheduler-1 chmod -R 777 /opt/airflow/assets
docker exec -u root safetrade_stocks_analysis_airflow_linux_os-airflow-triggerer-1 chmod -R 777 /opt/airflow/assets


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