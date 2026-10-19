# Weather Data ETL Pipeline

## 1. Project Overview

This project is a Python-based Weather Data Engineering pipeline that extracts hourly weather forecast data from the Open-Meteo API, transforms the response into a structured dataset, validates data quality, and stores the results in a CSV file.

The pipeline supports incremental loading and upsert logic to insert new records and update existing records when weather values change.

## 2. Technologies Used

- Python
- Pandas
- Requests
- REST API
- Open-Meteo API
- CSV
- Python Logging
- JupyterLab

## 3. Project Workflow

1. **Configuration:** Define the API endpoint, location coordinates, and weather parameters.
2. **Data Extraction:** Retrieve hourly weather forecast data from the Open-Meteo API.
3. **Data Transformation:** Convert the JSON response into a Pandas DataFrame.
4. **Data Validation:** Check required columns, missing values, duplicate timestamps, and acceptable weather value ranges.
5. **Incremental Loading and Upsert:** Insert new records and update existing records when weather values change.
6. **Data Storage:** Save the consolidated dataset to a CSV file.
7. **Logging and Error Handling:** Record execution events and handle API connection failures.

## 4. Dataset Description

| Column | Description |
|---|---|
| `weather_time` | Hourly weather timestamp |
| `temperature_c` | Temperature in degrees Celsius |
| `humidity_percent` | Relative humidity percentage |
| `wind_speed_kmh` | Wind speed in kilometres per hour |

## 5. Data Quality Checks

The pipeline checks for missing values, duplicate timestamps, and weather values outside the configured limits.

The stored dataset was verified to contain 49 records, with no duplicate timestamps or missing values.

## 6. Testing

- Tested successful API extraction.
- Tested repeated runs and incremental loading.
- Tested upsert logic for existing and new timestamps.
- Tested data quality validation.
- Tested an intentionally invalid API URL to check connection-failure handling.
- Restored the correct API URL and confirmed the pipeline ran successfully again.

## 7. How to Run

Install the required libraries:

```bash
pip install pandas requests
```

Run the pipeline from PowerShell:

```bash
python weather_pipeline.py
```

An internet connection is required to retrieve data from the Open-Meteo API.

## 8. Learning Outcomes

- Working with REST APIs and JSON data.
- Transforming data using Pandas.
- Implementing incremental loading and upsert logic.
- Applying data quality validation.
- Using logging and exception handling.
- Testing API connection failures.

## 9. Future Improvements

- Store data in a relational database.
- Schedule automated pipeline execution.
- Add automated tests and monitoring.
- Extend the pipeline using cloud storage and orchestration tools.
