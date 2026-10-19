import pandas as pd
import requests
import logging
from pathlib import Path

# Project folders
PROJECT_FOLDER = Path(
    r"C:\Users\hp\Desktop\DataEngineeringProject"
)

DATA_FOLDER = PROJECT_FOLDER / "Data"
LOG_FOLDER = PROJECT_FOLDER / "Logs"

# Create folders if they do not exist
DATA_FOLDER.mkdir(parents=True, exist_ok=True)
LOG_FOLDER.mkdir(parents=True, exist_ok=True)

# Input and output files
CSV_FILE = DATA_FOLDER / "weather_incremental.csv"
BACKUP_FILE = DATA_FOLDER / "weather_incremental_backup.csv"
LOG_FILE = LOG_FOLDER / "weather_pipeline.log"

# Open-Meteo API configuration
API_URL = "https://api.open-meteo.com/v1/forecast"

PARAMS = {
    "latitude": 11.001758,
    "longitude": 76.99468,
    "hourly": [
        "temperature_2m",
        "relative_humidity_2m",
        "wind_speed_10m"
    ],
    "forecast_days": 1,
    "timezone": "Asia/Kolkata"
}

# Logging configuration
logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True
)

logging.info("Weather pipeline configuration loaded")

print("Configuration loaded successfully!")
print("Project folder:", PROJECT_FOLDER)
print("CSV file:", CSV_FILE)
print("Log file:", LOG_FILE)


# Function to extract weather data from the API
def extract_weather_data():
    logging.info("Starting weather data extraction")

    try:
        response = requests.get(
            API_URL,
            params=PARAMS,
            timeout=30
        )

        response.raise_for_status()
        weather_json = response.json()

        weather_data = pd.DataFrame({
            "weather_time": weather_json["hourly"]["time"],
            "temperature_c": weather_json["hourly"]["temperature_2m"],
            "humidity_percent": weather_json["hourly"]["relative_humidity_2m"],
            "wind_speed_kmh": weather_json["hourly"]["wind_speed_10m"]
        })

        logging.info(
            "API extraction successful: %s records fetched",
            len(weather_data)
        )

        print("API extraction successful!")
        print("Records fetched:", len(weather_data))

        return weather_data

    except (requests.RequestException, KeyError, TypeError, ValueError):
        logging.exception("Weather data extraction failed")
        raise





def upsert_weather_data(new_data):
    """Insert new timestamps and update changed weather records."""

    logging.info("Starting weather data upsert")

    if CSV_FILE.exists():
        existing_data = pd.read_csv(CSV_FILE)
    else:
        existing_data = pd.DataFrame(columns=new_data.columns)

    # Remove duplicate timestamps from incoming data
    new_data = new_data.drop_duplicates(
        subset=["weather_time"],
        keep="last"
    ).copy()

    # Count existing records before the upsert
    records_before = len(existing_data)

    # Separate new timestamps from existing timestamps
    if existing_data.empty:
        new_timestamps = new_data["weather_time"]
        common_timestamps = pd.Series(dtype="object")
    else:
        existing_timestamps = set(existing_data["weather_time"])
        incoming_timestamps = set(new_data["weather_time"])

        new_timestamps = incoming_timestamps - existing_timestamps
        common_timestamps = incoming_timestamps & existing_timestamps

    inserted_count = len(new_timestamps)
    updated_count = 0

    # Use timestamp as the unique key
    existing_data = existing_data.set_index("weather_time")
    incoming_data = new_data.set_index("weather_time")

    # Update existing rows only when values have changed
    for timestamp in common_timestamps:
        old_values = existing_data.loc[timestamp]
        new_values = incoming_data.loc[timestamp]

        if not old_values.equals(new_values):
            existing_data.loc[timestamp] = new_values
            updated_count += 1

    # Add new timestamps
    new_rows = incoming_data.loc[
        incoming_data.index.isin(new_timestamps)
    ]

    final_data = pd.concat(
        [existing_data, new_rows]
    )

    final_data = final_data.reset_index()
    final_data = final_data.drop_duplicates(
        subset=["weather_time"],
        keep="last"
    )

    # Save the updated CSV
    final_data.to_csv(CSV_FILE, index=False)

    logging.info(
        "Upsert completed: inserted=%s, updated=%s, total=%s",
        inserted_count,
        updated_count,
        len(final_data)
    )

    print("\nUpsert completed successfully!")
    print("Records before:", records_before)
    print("New records inserted:", inserted_count)
    print("Existing records updated:", updated_count)
    print("Total records after:", len(final_data))

    return final_data




def validate_weather_data(data):
    """Validate weather records before saving."""

    required_columns = [
        "weather_time",
        "temperature_c",
        "humidity_percent",
        "wind_speed_kmh"
    ]

    # Check required columns
    missing_columns = [
        column for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Check missing values
    if data[required_columns].isnull().any().any():
        raise ValueError("Data contains missing values")

    # Check duplicate timestamps
    if data["weather_time"].duplicated().any():
        raise ValueError("Data contains duplicate timestamps")

    # Check temperature
    if not data["temperature_c"].between(-90, 60).all():
        raise ValueError("Temperature outside accepted range")

    # Check humidity
    if not data["humidity_percent"].between(0, 100).all():
        raise ValueError("Humidity outside valid range")

    # Check wind speed
    if (data["wind_speed_kmh"] < 0).any():
        raise ValueError("Wind speed cannot be negative")

    logging.info(
        "Data quality validation passed: %s records",
        len(data)
    )

    print("Data quality validation passed!")
    print("Records validated:", len(data))

    return True





# Main execution section
if __name__ == "__main__":
    try:
        new_data = extract_weather_data()

        print(new_data.head())

        # Validate data before saving
        validate_weather_data(new_data)

        # Upsert only if validation passes
        final_data = upsert_weather_data(new_data)

        print("\nLatest saved records:")
        print(final_data.tail())

        logging.info("Weather pipeline completed successfully")

    except Exception:
        logging.exception("Weather pipeline failed")
        print(
            "\nWeather pipeline failed. "
            "Please check the log file for details."
        )


