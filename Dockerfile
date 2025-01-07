FROM apache/airflow:2.7.3

USER root

# Set environment variables for better control
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV AIRFLOW_HOME=/opt/airflow

# Install system Chrome and dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        wget \
        gnupg2 \
        xvfb \
        x11vnc \
        xauth \
        xorg \
        openbox \
        libnss3 \
        libgbm1 \
        libasound2 \
        unzip \
        tesseract-ocr \
        libtesseract-dev \
        python3-dev \
        build-essential \
        chromium \
        chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Set up display environment variables
ENV DISPLAY=:99
ENV DISPLAY_WIDTH=1920
ENV DISPLAY_HEIGHT=1080

# Create Airflow directories and set permissions
RUN mkdir -p /opt/airflow/{logs,plugins,dags,assets} \
    && chown -R airflow:root /opt/airflow \
    && chmod -R 777 /opt/airflow \
    && chmod -R 777 /opt/airflow/assets

USER airflow

# Copy requirements file
COPY --chown=airflow:root requirements.txt /requirements.txt

# Install Python packages from requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Set Chrome-specific environment variables
ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    CHROME_BIN=/usr/bin/chromium \
    DISPLAY=:99