FROM python:3.12-slim

# Install Chromium + ChromeDriver for Selenium
RUN apt-get update && \
    apt-get install -y chromium chromium-driver && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /tests

# Install Python dependencies for Selenium tests
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the selenium test code
COPY . .

# Default command: run pytest
CMD ["pytest", "-v"]
