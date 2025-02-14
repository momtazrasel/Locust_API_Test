import time
import csv
import pandas as pd
import requests
import random

from jinja2 import environment
from locust import User, task, events

# Load URLs from Excel file
EXCEL_FILE = "urls.xlsx"
URLS = pd.read_excel(EXCEL_FILE)["URL"].tolist()

# CSV Logging Setup
CSV_FILE = "api_test_results.csv"
CSV_HEADERS = ["URL", "Status", "Response Code", "Request Timestamp", "Response Timestamp", "Request Duration", "Response Body"]

# Create CSV file and write headers
with open(CSV_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(CSV_HEADERS)

class RateLimitedUser(User):
    def __init__(self, environment):
        super().__init__(environment)
        self.rps = 1  # Start with 1 RPS
        self.start_time = time.time()

    def wait_time(self):
        return 0  # No waiting (we control timing manually)

    @task
    def fetch_url(self):
        elapsed_time = time.time() - self.start_time
        max_rps = 65
        ramp_up_time = 600  # 10 minutes (600 seconds)

        # Gradually increase RPS
        if elapsed_time < ramp_up_time:
            self.rps = int((elapsed_time / ramp_up_time) * max_rps)
        else:
            self.rps = max_rps

        interval = 1 / self.rps  # Time between requests
        request_time = time.time()

        url = random.choice(URLS)  # Select a random URL from Excel
        try:
            response = requests.get(url)
            response_time = time.time()
            duration = response_time - request_time
            status = "success" if response.status_code == 200 else "failure"

            # Save results to CSV
            with open(CSV_FILE, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([url, status, response.status_code, request_time, response_time, duration, response.text[:100]])

        except Exception as e:
            response_time = time.time()
            with open(CSV_FILE, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([url, "failure", "N/A", request_time, response_time, "N/A", str(e)])

        # Sleep to maintain exact RPS
        time.sleep(max(0, interval - (time.time() - request_time)))

# Stop test if failure rate exceeds threshold
@events.request.add_listener
def on_request(request_type, name, response_time, response_length, response, exception, context, **kwargs):
    if exception or (response and response.status_code >= 500):
        failure_count = getattr(environment.runner, "failure_count", 0) + 1
        environment.runner.failure_count = failure_count
        if failure_count > 100:  # Stop if too many failures
            environment.runner.quit()
