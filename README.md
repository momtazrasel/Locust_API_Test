# Locust_API_Test
# API Stress Test with Locust & Excel

This project is designed to **stress test a web scraping API** by sending requests at a controlled rate, gradually scaling up to **65 requests per second (RPS)** over **10 minutes** and sustaining that rate for **25 minutes**. The test reads URLs from an Excel file and logs results in a CSV file.

## Features
✅ **Gradual RPS Scaling**: Starts slow and reaches **65 RPS in 10 minutes**  
✅ **Failure Monitoring**: Stops automatically if too many failures occur  
✅ **Excel Integration**: Reads URLs from `urls.xlsx`  
✅ **CSV Logging**: Saves request details in `api_test_results.csv`  
✅ **Automated Rate Control**: Ensures exact RPS without concurrency  

## Requirements
- Python 3.7+
- PyCharm (optional, but recommended)

## Setup
### Install Dependencies
```sh
pip install locust pandas openpyxl requests
```

### Run the Test
```sh
locust -f locustfile.py --headless --run-time 35m
```

## CSV Output (`api_test_results.csv`)
Logs the test results with details such as URL, status, response code, timestamps, duration, and response body.

## Stopping the Test
Press `CTRL + C` to stop manually.

## Future Enhancements
- Add support for **custom headers & payloads**
- Implement **distributed testing** across multiple machines
- Integrate with **Grafana for real-time monitoring**

📌 **Contributions & Issues**: Feel free to **fork this repo, submit pull requests, or report issues!** 🚀

