FROM python:3.11-slim

# Install Firefox and dependencies
RUN apt-get update && apt-get install -y \
    firefox-esr wget unzip curl \
    libgtk-3-0 libdbus-glib-1-2 libxt6 libxss1 libasound2 && \
    rm -rf /var/lib/apt/lists/*

# Install GeckoDriver (latest release)
RUN GECKO_VER=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep '"tag_name":' | cut -d '"' -f 4) && \
    wget -q "https://github.com/mozilla/geckodriver/releases/download/${GECKO_VER}/geckodriver-${GECKO_VER}-linux64.tar.gz" && \
    tar -xzf geckodriver-*.tar.gz -C /usr/local/bin && \
    rm geckodriver-*.tar.gz

# Install Selenium
RUN pip install selenium

# Add your script
WORKDIR /app
COPY ghost_admin.py /app/

CMD ["python3", "ghost_admin.py"]
