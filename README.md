# stock_recommendation_managed_by_airflow


1. First, add your user to the Docker group:
sudo usermod -aG docker $USER

2. Verify your user is in the Docker group:
groups $USER

3. Apply the new group membership:
newgrp docker


THEN proceed with the Docker service restart steps:
1. First, stop both the Docker service AND socket in the correct order:
sudo systemctl stop docker.service
sudo systemctl stop docker.socket

Make sure both are stopped by checking their status:
sudo systemctl status docker.service
sudo systemctl status docker.socket


Good, both Docker service and socket are now properly stopped. Let's restart Docker fresh:
1. Start the Docker socket first:
sudo systemctl start docker.socket


2. Then start the Docker service:
sudo systemctl start docker


3. Verify both are running:
sudo systemctl status docker


4. Let's also make sure the Docker socket has the correct permissions:
sudo chmod 666 /var/run/docker.sock


5. Finally:
docker-compose build --no-cache
