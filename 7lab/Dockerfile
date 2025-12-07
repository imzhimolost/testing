FROM jenkins/jenkins:lts

USER root

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        qemu-system-arm \
        wget \
        git \
        python3 \
        python3-pip \
        python3-venv \
        chromium-driver \
        firefox-esr \
        xvfb \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux64.tar.gz \
    && tar -xvzf geckodriver-v0.35.0-linux64.tar.gz \
    && chmod +x geckodriver \
    && mv geckodriver /usr/local/bin/ \
    && rm geckodriver-v0.35.0-linux64.tar.gz

RUN pip3 install --no-cache-dir --break-system-packages \
        pytest \
        requests \
        selenium \
        locust

USER jenkins