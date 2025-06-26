FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

WORKDIR /app
COPY ghost_admin.py /app/

# Install only Chromium
RUN pip install playwright && playwright install chromium

CMD ["python3", "ghost_admin.py"]

