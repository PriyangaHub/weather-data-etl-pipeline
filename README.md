\# Weather Data ETL Pipeline



\## 1. Project Overview



This project is a Python-based Weather Data Engineering pipeline that extracts hourly weather forecast data from the Open-Meteo API, transforms the response into a structured dataset, validates data quality, and stores the results in a CSV file.



The pipeline supports incremental loading and upsert logic to insert new records and update existing records when weather values change.



\## 2. Technologies Used



\- Python

\- Pandas

\- Requests

\- REST API

\- Open-Meteo API

\- CSV

\- Python Logging

\- JupyterLab



\## 3. Project Workflow



1\. \*\*Configuration:\*\* Define the API endpoint, location coordinates, and weather parameters.

2\. \*\*Data Extraction:\*\* Retrieve hourly weather

