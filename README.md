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

   # Google Drive settings
   GOOGLE_CREDENTIALS_JSON=safe-trade-byai-1ad3bbad3477.json
   GOOGLE_CSV_FILE_URL='https://docs.google.com/spreadsheets/d/1w1_v4Pc_joAh9ymCGri0jJVSSIg-_3NzBOpR62Mu37s/edit?gid=0#gid=0'
   GOOGLE_FOLDER_ID=1NyxrwJCL77pSmtyP_fIwAayt73KCIf_s
   ```
2. Attach a assets/credentials/<google_api_key>.json file. The file is not in the repo and is for access to google drive & sheets (see below for how to create it)
3. share the google sheet and drive folder with the service account email (see below for how to create it)
4. Initialize airflow database:
   ```bash
   docker-compose up airflow-init
   ```
5. Start all airflow services in detached mode with latest changes:
   ```bash
   docker-compose up -d --build
   ```
6. This container will own by airflow user, so you need to set the permissions to write in the directory :
   ```bash
   sudo chmod -R o+w dags/
   sudo chmod -R o+w logs/
   sudo chmod -R o+w plugins/
   sudo chmod -R o+w assets/
   ```
7. see running containers:
   ```bash
   docker ps
   ```
8. Stop all airflow services:
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


# How to Create a JSON Credentials File in GCP Console

📝 Follow these steps to create a JSON credentials file for accessing Google Drive and Google Sheets:

## 1️⃣ Enable Required APIs
1. Open the Google Cloud Console
2. Go to `APIs & Services > Library`
3. Enable the following APIs:
   - ✅ Google Drive API
   - ✅ Google Sheets API

## 2️⃣ Create a Service Account
1. Navigate to `IAM & Admin > Service Accounts`
2. Click `Create Service Account`
3. Provide a name and description for the service account
4. Assign a role:
   - 🔑 For full access: `Editor`
   - 🔒 For restricted access: Assign `Cloud Storage Object Viewer` and `Viewer` roles
5. Click `Continue`, then `Done`

## 3️⃣ Generate the JSON Credentials File
1. Find the service account in `IAM & Admin > Service Accounts`
2. Click the service account name, then go to the `Keys` tab
3. Click `Add Key > Create New Key`
4. Select `JSON` as the key type and click `Create`
5. ⬇️ The JSON file will be downloaded to your computer

## 4️⃣ Share the Google Sheet with the Service Account
1. Open the Google Sheet
2. Click `Share`
3. Click `Add people`
4. Add the service account email
5. Assign the `Viewer` role
6. Click `Send`

## 5️⃣ Share the Google Drive Folder with the Service Account
1. Open the Google Drive Folder
2. Click `Share`
3. Click `Add people`
4. Add the service account email
5. Assign the `Viewer` role
6. Click `Send`
